import base64
from typing import Any

import httpx
from nacl import encoding, public

from .settings import GITHUB_OWNER, GITHUB_TOKEN


API_ROOT = "https://api.github.com"
API_VERSION = "2022-11-28"
TIMEOUT = 25.0


class GitHubError(RuntimeError):
    pass


def _headers() -> dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "sly-director-github-mcp",
    }


def request(
    method: str,
    path: str,
    *,
    expected: tuple[int, ...] = (200,),
    params: dict[str, Any] | None = None,
    json: Any = None,
    follow_redirects: bool = True,
) -> httpx.Response:
    try:
        response = httpx.request(
            method,
            f"{API_ROOT}{path}",
            headers=_headers(),
            params=params,
            json=json,
            timeout=TIMEOUT,
            follow_redirects=follow_redirects,
        )
    except httpx.TimeoutException as exc:
        raise GitHubError(f"GitHub request timed out: {method} {path}") from exc
    except httpx.HTTPError as exc:
        raise GitHubError(f"GitHub transport error: {method} {path}: {exc}") from exc

    if response.status_code not in expected:
        try:
            detail = response.json()
        except Exception:
            detail = response.text[:2000]
        raise GitHubError(
            f"GitHub returned HTTP {response.status_code} for {method} {path}: {detail}"
        )
    return response


def repo_path(repo: str, suffix: str = "") -> str:
    repo = repo.strip().strip("/")
    if not repo or "/" in repo:
        raise ValueError("repo must be the repository name only, without an owner")
    suffix = suffix if suffix.startswith("/") or not suffix else f"/{suffix}"
    return f"/repos/{GITHUB_OWNER}/{repo}{suffix}"


def repo_info(repo: str) -> dict[str, Any]:
    return request("GET", repo_path(repo)).json()


def default_branch(repo: str) -> str:
    return str(repo_info(repo).get("default_branch") or "main")


def get_file(repo: str, path: str, ref: str | None = None) -> dict[str, Any] | None:
    params = {"ref": ref} if ref else None
    response = httpx.get(
        f"{API_ROOT}{repo_path(repo, f'/contents/{path}')}" ,
        headers=_headers(),
        params=params,
        timeout=TIMEOUT,
    )
    if response.status_code == 404:
        return None
    if response.status_code != 200:
        try:
            detail = response.json()
        except Exception:
            detail = response.text[:2000]
        raise GitHubError(f"GitHub returned HTTP {response.status_code}: {detail}")
    data = response.json()
    if isinstance(data, list):
        raise GitHubError("Requested path is a directory, not a file")
    content = data.get("content", "")
    if data.get("encoding") == "base64" and content:
        data["decoded_content"] = base64.b64decode(content).decode("utf-8", errors="replace")
    else:
        data["decoded_content"] = ""
    return data


def branch_sha(repo: str, branch: str) -> str:
    data = request("GET", repo_path(repo, f"/git/ref/heads/{branch}")).json()
    return str(data["object"]["sha"])


def create_branch(repo: str, new_branch: str, from_branch: str) -> dict[str, Any]:
    sha = branch_sha(repo, from_branch)
    return request(
        "POST",
        repo_path(repo, "/git/refs"),
        expected=(201,),
        json={"ref": f"refs/heads/{new_branch}", "sha": sha},
    ).json()


def put_file(repo: str, branch: str, path: str, content: str, message: str) -> dict[str, Any]:
    existing = get_file(repo, path, branch)
    payload: dict[str, Any] = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
        "branch": branch,
    }
    if existing and existing.get("sha"):
        payload["sha"] = existing["sha"]
    return request(
        "PUT",
        repo_path(repo, f"/contents/{path}"),
        expected=(200, 201),
        json=payload,
    ).json()


def delete_file(repo: str, branch: str, path: str, message: str) -> dict[str, Any]:
    existing = get_file(repo, path, branch)
    if not existing or not existing.get("sha"):
        raise GitHubError(f"File not found on branch {branch}: {path}")
    return request(
        "DELETE",
        repo_path(repo, f"/contents/{path}"),
        expected=(200,),
        json={"message": message, "sha": existing["sha"], "branch": branch},
    ).json()


def encrypt_secret(public_key_b64: str, plaintext: str) -> str:
    key = public.PublicKey(public_key_b64.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(key)
    return base64.b64encode(sealed_box.encrypt(plaintext.encode("utf-8"))).decode("ascii")
