"""
一键创建 GitHub 数据存储仓库
用于 CHATSAM 项目的数据持久化

使用方法:
1. 设置环境变量 GITHUB_TOKEN (你的 GitHub Personal Access Token)
2. 运行脚本: python scripts/create_data_repo.py

或者直接传入参数:
python scripts/create_data_repo.py --token ghp_xxx --repo-name my-chatsam-data
"""

import argparse
import json
import os
import sys
import requests
from pathlib import Path


GITHUB_API_URL = "https://api.github.com"


def get_github_username(token: str) -> str:
    """获取 GitHub 用户名"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(f"{GITHUB_API_URL}/user", headers=headers)
    if response.status_code != 200:
        raise Exception(f"获取用户信息失败: {response.text}")
    return response.json()["login"]


def create_repository(token: str, username: str, repo_name: str, private: bool = True) -> dict:
    """创建 GitHub 仓库"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "description": "CHATSAM Data Storage - 用于存储账号和用户数据",
        "private": private,
        "auto_init": False
    }
    response = requests.post(f"{GITHUB_API_URL}/user/repos", headers=headers, json=data)
    if response.status_code == 201:
        print(f"✅ 仓库创建成功: {username}/{repo_name}")
        return response.json()
    elif response.status_code == 422:
        raise Exception(f"仓库已存在: {username}/{repo_name}")
    else:
        raise Exception(f"创建仓库失败: {response.text}")


def create_file_in_repo(token: str, username: str, repo_name: str, file_path: str, content: dict, message: str) -> bool:
    """在仓库中创建文件"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"{GITHUB_API_URL}/repos/{username}/{repo_name}/contents/{file_path}"
    data = {
        "message": message,
        "content": base64_encode(json.dumps(content, ensure_ascii=False, indent=2))
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"✅ 文件创建成功: {file_path}")
        return True
    else:
        raise Exception(f"创建文件失败: {response.text}")


def base64_encode(content: str) -> str:
    """Base64 编码"""
    import base64
    return base64.b64encode(content.encode("utf-8")).decode("utf-8")


def main():
    parser = argparse.ArgumentParser(description="一键创建 CHATSAM 数据存储仓库")
    parser.add_argument("--token", help="GitHub Personal Access Token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--repo-name", help="仓库名称", default="chatsam-data")
    parser.add_argument("--public", help="创建公开仓库", action="store_true", default=False)
    
    args = parser.parse_args()
    
    if not args.token:
        print("❌ 错误: 请提供 GitHub Token")
        print("方式 1: 设置环境变量 GITHUB_TOKEN")
        print("方式 2: 使用 --token 参数")
        print("\n示例:")
        print("  python scripts/create_data_repo.py --token ghp_xxx --repo-name my-data")
        sys.exit(1)
    
    try:
        print("🚀 开始创建数据仓库...")
        
        username = get_github_username(args.token)
        print(f"👤 GitHub 用户: {username}")
        
        repo_info = create_repository(
            token=args.token,
            username=username,
            repo_name=args.repo_name,
            private=not args.public
        )
        
        accounts_data = {"items": []}
        auth_keys_data = {"items": []}
        
        create_file_in_repo(
            token=args.token,
            username=username,
            repo_name=args.repo_name,
            file_path="accounts.json",
            content=accounts_data,
            message="init: accounts.json"
        )
        
        create_file_in_repo(
            token=args.token,
            username=username,
            repo_name=args.repo_name,
            file_path="auth_keys.json",
            content=auth_keys_data,
            message="init: auth_keys.json"
        )
        
        print("\n" + "=" * 50)
        print("🎉 数据仓库创建完成!")
        print("=" * 50)
        print(f"\n📦 仓库地址: https://github.com/{username}/{args.repo_name}")
        print("\n📋 下一步: 在 HuggingFace Space 配置 Secrets")
        print("-" * 50)
        print(f"STORAGE_BACKEND = git")
        print(f"GIT_REPO_URL = https://github.com/{username}/{args.repo_name}.git")
        print(f"GIT_TOKEN = {args.token[:10]}... (你的完整 Token)")
        print("-" * 50)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()