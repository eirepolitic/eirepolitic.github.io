from typing import Any

from mangum import Mangum
from mcp.server import MCPServer
from mcp.server.auth.settings import AuthSettings
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import AnyHttpUrl
from starlette.requests import Request
from starlette.responses import JSONResponse

from .auth import CognitoTokenVerifier
from .github_client import (
    GITHUB_OWNER,
    create_branch as gh_create_branch,
    default_branch,
    delete_file as gh_delete_file,
    encrypt_secret,
    get_file,
    put_file,
    repo_info,
    repo_path,
    request,
)
from .settings import BRANCH_PREFIX, COGNITO_ISSUER, DEFAULT_BASE_BRANCH, PUBLIC_MCP_HOST, PUBLIC_MCP_URL


mcp = MCPServer(
    "Sly Director GitHub",
    instructions=(
        "GitHub repository operations for Sly Director. The GitHub owner is configured "
        "on the server. Tool parameters named repo always expect only the repository name."
    ),
    token_verifier=CognitoTokenVerifier(),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl(COGNITO_ISSUER),
        resource_server_url=AnyHttpUrl(PUBLIC_MCP_URL),
        required_scopes=["openid"],
    ),
)


def _branch(name: str) -> str:
    name = name.strip().strip("/")
    if not name:
        raise ValueError("branch name cannot be empty")
    if BRANCH_PREFIX and not name.startswith(BRANCH_PREFIX):
        name = f"{BRANCH_PREFIX}{name}"
    return name


@mcp.custom_route("/health", methods=["GET"])
async def health(_: Request) -> JSONResponse:
    return JSONResponse({"ok": True, "service": "sly-director-github-mcp", "owner": GITHUB_OWNER})


@mcp.tool()
def get_repository(repo: str) -> dict[str, Any]:
    """Get basic metadata for a repository. Pass only the repository name."""
    data = repo_info(repo)
    return {
        "name": data.get("name"),
        "full_name": data.get("full_name"),
        "private": data.get("private"),
        "default_branch": data.get("default_branch"),
        "html_url": data.get("html_url"),
        "archived": data.get("archived"),
    }


@mcp.tool()
def read_file(repo: str, path: str, ref: str | None = None) -> dict[str, Any]:
    """Read one text file from a repository branch, tag, or commit."""
    data = get_file(repo, path, ref)
    if not data:
        raise RuntimeError(f"File not found: {path}")
    return {
        "repo": repo,
        "path": path,
        "ref": ref,
        "sha": data.get("sha"),
        "size": data.get("size"),
        "content": data.get("decoded_content", ""),
        "html_url": data.get("html_url"),
    }


@mcp.tool()
def list_repository_tree(
    repo: str,
    ref: str | None = None,
    recursive: bool = True,
    path_prefix: str | None = None,
) -> dict[str, Any]:
    """List files and directories in a repository tree."""
    target = ref or default_branch(repo)
    commit = request("GET", repo_path(repo, f"/commits/{target}")).json()
    tree_sha = commit["commit"]["tree"]["sha"]
    params = {"recursive": "1"} if recursive else None
    data = request("GET", repo_path(repo, f"/git/trees/{tree_sha}"), params=params).json()
    items = data.get("tree", [])
    if path_prefix:
        prefix = path_prefix.strip("/")
        items = [item for item in items if str(item.get("path", "")).startswith(prefix)]
    return {
        "repo": repo,
        "ref": target,
        "truncated": data.get("truncated", False),
        "count": len(items),
        "items": items,
    }


@mcp.tool()
def search_repository(repo: str, query: str, per_page: int = 25, page: int = 1) -> dict[str, Any]:
    """Search code within one repository."""
    data = request(
        "GET",
        "/search/code",
        params={"q": f"{query} repo:{GITHUB_OWNER}/{repo}", "per_page": per_page, "page": page},
    ).json()
    return {
        "repo": repo,
        "query": query,
        "total_count": data.get("total_count", 0),
        "incomplete_results": data.get("incomplete_results", False),
        "items": [
            {
                "name": item.get("name"),
                "path": item.get("path"),
                "sha": item.get("sha"),
                "html_url": item.get("html_url"),
            }
            for item in data.get("items", [])
        ],
    }


@mcp.tool()
def list_branches(repo: str, per_page: int = 100, page: int = 1) -> list[dict[str, Any]]:
    """List repository branches."""
    return request(
        "GET",
        repo_path(repo, "/branches"),
        params={"per_page": per_page, "page": page},
    ).json()


@mcp.tool()
def create_branch(repo: str, new_branch: str, from_branch: str | None = None) -> dict[str, Any]:
    """Create a working branch. The configured branch prefix is added automatically."""
    source = from_branch or default_branch(repo) or DEFAULT_BASE_BRANCH
    return gh_create_branch(repo, _branch(new_branch), source)


@mcp.tool()
def delete_branch(repo: str, branch: str) -> dict[str, str]:
    """Delete a repository branch created for work."""
    target = _branch(branch)
    request("DELETE", repo_path(repo, f"/git/refs/heads/{target}"), expected=(204,))
    return {"repo": repo, "branch": target, "status": "deleted"}


@mcp.tool()
def upsert_file(
    repo: str,
    path: str,
    content: str,
    commit_message: str,
    branch: str,
) -> dict[str, Any]:
    """Create or update a file on an existing working branch."""
    target = _branch(branch)
    result = put_file(repo, target, path, content, commit_message)
    return {
        "repo": repo,
        "path": path,
        "branch": target,
        "content": result.get("content"),
        "commit": result.get("commit"),
    }


@mcp.tool()
def upsert_files(
    repo: str,
    files: list[dict[str, str]],
    commit_message: str,
    branch: str,
) -> dict[str, Any]:
    """Create or update several text files on one working branch."""
    target = _branch(branch)
    results = []
    for item in files:
        path = item.get("path", "").strip()
        if not path or "content" not in item:
            raise ValueError("Each files item must contain path and content")
        result = put_file(repo, target, path, item["content"], f"{commit_message}: {path}")
        results.append({"path": path, "commit_sha": (result.get("commit") or {}).get("sha")})
    return {"repo": repo, "branch": target, "files": results}


@mcp.tool()
def delete_file(repo: str, path: str, commit_message: str, branch: str) -> dict[str, Any]:
    """Delete a file from an existing working branch."""
    target = _branch(branch)
    result = gh_delete_file(repo, target, path, commit_message)
    return {"repo": repo, "path": path, "branch": target, "commit": result.get("commit")}


@mcp.tool()
def list_pull_requests(
    repo: str,
    state: str = "open",
    head: str | None = None,
    base: str | None = None,
    per_page: int = 30,
    page: int = 1,
) -> list[dict[str, Any]]:
    """List pull requests."""
    params: dict[str, Any] = {"state": state, "per_page": per_page, "page": page}
    if head:
        params["head"] = head
    if base:
        params["base"] = base
    return request("GET", repo_path(repo, "/pulls"), params=params).json()


@mcp.tool()
def get_pull_request(repo: str, number: int) -> dict[str, Any]:
    """Get one pull request."""
    return request("GET", repo_path(repo, f"/pulls/{number}")).json()


@mcp.tool()
def create_pull_request(
    repo: str,
    title: str,
    body: str,
    head_branch: str,
    base_branch: str | None = None,
    draft: bool = False,
) -> dict[str, Any]:
    """Create a pull request from a Sly Director working branch."""
    return request(
        "POST",
        repo_path(repo, "/pulls"),
        expected=(201,),
        json={
            "title": title,
            "body": body,
            "head": _branch(head_branch),
            "base": base_branch or default_branch(repo),
            "draft": draft,
        },
    ).json()


@mcp.tool()
def update_pull_request(
    repo: str,
    number: int,
    title: str | None = None,
    body: str | None = None,
    state: str | None = None,
    base_branch: str | None = None,
) -> dict[str, Any]:
    """Update pull-request title, body, state, or base branch."""
    payload: dict[str, Any] = {}
    if title is not None:
        payload["title"] = title
    if body is not None:
        payload["body"] = body
    if state is not None:
        payload["state"] = state
    if base_branch is not None:
        payload["base"] = base_branch
    return request("PATCH", repo_path(repo, f"/pulls/{number}"), json=payload).json()


@mcp.tool()
def merge_pull_request(
    repo: str,
    number: int,
    merge_method: str = "squash",
    commit_title: str | None = None,
    commit_message: str | None = None,
    sha: str | None = None,
) -> dict[str, Any]:
    """Merge a pull request using merge, squash, or rebase."""
    payload: dict[str, Any] = {"merge_method": merge_method}
    if commit_title:
        payload["commit_title"] = commit_title
    if commit_message:
        payload["commit_message"] = commit_message
    if sha:
        payload["sha"] = sha
    return request(
        "PUT",
        repo_path(repo, f"/pulls/{number}/merge"),
        expected=(200, 405, 409),
        json=payload,
    ).json()


@mcp.tool()
def list_workflows(repo: str, per_page: int = 100, page: int = 1) -> dict[str, Any]:
    """List GitHub Actions workflows."""
    return request(
        "GET",
        repo_path(repo, "/actions/workflows"),
        params={"per_page": per_page, "page": page},
    ).json()


@mcp.tool()
def list_workflow_runs(
    repo: str,
    workflow_id: str | None = None,
    branch: str | None = None,
    event: str | None = None,
    status: str | None = None,
    per_page: int = 20,
    page: int = 1,
) -> dict[str, Any]:
    """List GitHub Actions workflow runs, optionally filtered."""
    suffix = f"/actions/workflows/{workflow_id}/runs" if workflow_id else "/actions/runs"
    params: dict[str, Any] = {"per_page": per_page, "page": page}
    if branch:
        params["branch"] = branch
    if event:
        params["event"] = event
    if status:
        params["status"] = status
    return request("GET", repo_path(repo, suffix), params=params).json()


@mcp.tool()
def get_workflow_run(repo: str, run_id: int) -> dict[str, Any]:
    """Get one GitHub Actions workflow run."""
    return request("GET", repo_path(repo, f"/actions/runs/{run_id}")).json()


@mcp.tool()
def list_workflow_run_jobs(repo: str, run_id: int, per_page: int = 100, page: int = 1) -> dict[str, Any]:
    """List jobs and steps for a workflow run."""
    return request(
        "GET",
        repo_path(repo, f"/actions/runs/{run_id}/jobs"),
        params={"per_page": per_page, "page": page},
    ).json()


@mcp.tool()
def get_workflow_run_logs(repo: str, run_id: int) -> dict[str, Any]:
    """Get the temporary GitHub download URL for a workflow-run log archive."""
    response = request(
        "GET",
        repo_path(repo, f"/actions/runs/{run_id}/logs"),
        expected=(302, 307),
        follow_redirects=False,
    )
    return {"repo": repo, "run_id": run_id, "download_url": response.headers.get("location")}


@mcp.tool()
def list_workflow_run_artifacts(repo: str, run_id: int, per_page: int = 100, page: int = 1) -> dict[str, Any]:
    """List artifacts produced by a workflow run."""
    return request(
        "GET",
        repo_path(repo, f"/actions/runs/{run_id}/artifacts"),
        params={"per_page": per_page, "page": page},
    ).json()


@mcp.tool()
def dispatch_workflow(
    repo: str,
    workflow_id: str,
    ref: str,
    inputs: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Start a workflow that supports workflow_dispatch."""
    request(
        "POST",
        repo_path(repo, f"/actions/workflows/{workflow_id}/dispatches"),
        expected=(204,),
        json={"ref": ref, "inputs": inputs or {}},
    )
    return {"repo": repo, "workflow_id": workflow_id, "ref": ref, "status": "dispatched"}


@mcp.tool()
def enable_workflow(repo: str, workflow_id: str) -> dict[str, str]:
    """Enable a GitHub Actions workflow."""
    request("PUT", repo_path(repo, f"/actions/workflows/{workflow_id}/enable"), expected=(204,))
    return {"repo": repo, "workflow_id": workflow_id, "status": "enabled"}


@mcp.tool()
def disable_workflow(repo: str, workflow_id: str) -> dict[str, str]:
    """Disable a GitHub Actions workflow."""
    request("PUT", repo_path(repo, f"/actions/workflows/{workflow_id}/disable"), expected=(204,))
    return {"repo": repo, "workflow_id": workflow_id, "status": "disabled"}


@mcp.tool()
def set_actions_variable(repo: str, name: str, value: str) -> dict[str, str]:
    """Create or update a repository Actions variable."""
    create = request(
        "POST",
        repo_path(repo, "/actions/variables"),
        expected=(201, 409),
        json={"name": name, "value": value},
    )
    if create.status_code == 409:
        request(
            "PATCH",
            repo_path(repo, f"/actions/variables/{name}"),
            expected=(204,),
            json={"name": name, "value": value},
        )
        status = "updated"
    else:
        status = "created"
    return {"repo": repo, "name": name, "status": status}


@mcp.tool()
def delete_actions_variable(repo: str, name: str) -> dict[str, str]:
    """Delete a repository Actions variable."""
    request("DELETE", repo_path(repo, f"/actions/variables/{name}"), expected=(204,))
    return {"repo": repo, "name": name, "status": "deleted"}


@mcp.tool()
def set_actions_secret(repo: str, name: str, plaintext_value: str) -> dict[str, str]:
    """Create or update a repository Actions secret. The plaintext value is sent only to GitHub."""
    key_data = request("GET", repo_path(repo, "/actions/secrets/public-key")).json()
    encrypted_value = encrypt_secret(key_data["key"], plaintext_value)
    response = request(
        "PUT",
        repo_path(repo, f"/actions/secrets/{name}"),
        expected=(201, 204),
        json={"encrypted_value": encrypted_value, "key_id": key_data["key_id"]},
    )
    return {"repo": repo, "name": name, "status": "created" if response.status_code == 201 else "updated"}


@mcp.tool()
def delete_actions_secret(repo: str, name: str) -> dict[str, str]:
    """Delete a repository Actions secret."""
    request("DELETE", repo_path(repo, f"/actions/secrets/{name}"), expected=(204,))
    return {"repo": repo, "name": name, "status": "deleted"}


transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=[PUBLIC_MCP_HOST, f"{PUBLIC_MCP_HOST}:*"],
    allowed_origins=["https://claude.ai", "https://www.claude.ai"],
)

app = mcp.streamable_http_app(
    streamable_http_path="/mcp",
    stateless_http=True,
    json_response=True,
    transport_security=transport_security,
)

handler = Mangum(app, lifespan="auto")
