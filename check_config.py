#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLMOps配置检查脚本
用于检查项目配置的完整性和正确性
"""

import os
import sys
from typing import Dict, List, Tuple

def check_required_config() -> List[str]:
    """检查必需配置"""
    required_configs = [
        'JWT_SECRET_KEY',
        'SQLALCHEMY_DATABASE_URI',
        'REDIS_HOST',
    ]
    
    missing_configs = []
    for config in required_configs:
        if not os.getenv(config):
            missing_configs.append(config)
    
    return missing_configs

def check_optional_config() -> Dict[str, List[str]]:
    """检查可选配置"""
    optional_configs = {
        '数据库配置': [
            'SQLALCHEMY_POOL_SIZE',
            'SQLALCHEMY_POOL_RECYCLE',
            'SQLALCHEMY_ECHO',
        ],
        'Redis配置': [
            'REDIS_PORT',
            'REDIS_USERNAME',
            'REDIS_PASSWORD',
            'REDIS_DB',
            'REDIS_USE_SSL',
        ],
        'Celery配置': [
            'CELERY_BROKER_DB',
            'CELERY_RESULT_BACKEND_DB',
            'CELERY_TASK_IGNORE_RESULT',
            'CELERY_RESULT_EXPIRES',
            'CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP',
        ],
        'Weaviate配置': [
            'WEAVIATE_URL',
            'WEAVIATE_API_KEY',
        ],
        'JWT配置': [
            'JWT_SECRET_KEY',
        ],
        '腾讯云COS配置': [
            'COS_REGION',
            'COS_BUCKET',
            'COS_SECRET_ID',
            'COS_SECRET_KEY',
            'COS_SCHEME',
            'COS_DOMAIN',
        ],
        'GitHub OAuth配置': [
            'GITHUB_CLIENT_ID',
            'GITHUB_CLIENT_SECRET',
            'GITHUB_REDIRECT_URI',
        ],
        '语言模型API密钥': [
            'OPENAI_API_KEY',
            'ANTHROPIC_API_KEY',
            'MOONSHOT_API_KEY',
            'DEEPSEEK_API_KEY',
        ],
        '内置工具API密钥': [
            'GAODE_API_KEY',
            'SERPER_API_KEY',
            'GOOGLE_API_KEY',
        ],
        '应用配置': [
            'ASSISTANT_AGENT_ID',
            'WTF_CSRF_ENABLED',
            'FLASK_APP',
            'FLASK_ENV',
        ],
    }
    
    config_status = {}
    for category, configs in optional_configs.items():
        configured = []
        missing = []
        for config in configs:
            if os.getenv(config):
                configured.append(config)
            else:
                missing.append(config)
        config_status[category] = {
            'configured': configured,
            'missing': missing
        }
    
    return config_status

def check_database_connection() -> bool:
    """检查数据库连接"""
    try:
        from config import Config
        conf = Config()
        return bool(conf.SQLALCHEMY_DATABASE_URI)
    except Exception:
        return False

def check_redis_connection() -> bool:
    """检查Redis连接"""
    try:
        from config import Config
        conf = Config()
        return bool(conf.REDIS_HOST)
    except Exception:
        return False

def check_weaviate_connection() -> Tuple[bool, str]:
    """检查Weaviate连接"""
    weaviate_url = os.getenv('WEAVIATE_URL')
    weaviate_key = os.getenv('WEAVIATE_API_KEY')
    
    if not weaviate_url or not weaviate_key:
        return False, "未配置Weaviate URL或API密钥"
    
    try:
        import weaviate
        from weaviate.auth import AuthApiKey
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=AuthApiKey(weaviate_key),
        )
        client.close()
        return True, "连接成功"
    except Exception as e:
        return False, f"连接失败: {str(e)}"

def main():
    """主函数"""
    print("🔍 LLMOps配置检查工具")
    print("=" * 50)
    
    # 检查必需配置
    print("\n🔴 必需配置检查:")
    missing_required = check_required_config()
    if missing_required:
        print("❌ 缺少必需配置:")
        for config in missing_required:
            print(f"   - {config}")
        print("\n⚠️  警告: 缺少必需配置，服务可能无法正常启动！")
    else:
        print("✅ 所有必需配置已设置")
    
    # 检查可选配置
    print("\n🟡 可选配置检查:")
    optional_status = check_optional_config()
    
    for category, status in optional_status.items():
        configured_count = len(status['configured'])
        total_count = len(status['configured']) + len(status['missing'])
        
        if configured_count == 0:
            print(f"⚪ {category}: 未配置 ({configured_count}/{total_count})")
        elif configured_count == total_count:
            print(f"✅ {category}: 完全配置 ({configured_count}/{total_count})")
        else:
            print(f"🟡 {category}: 部分配置 ({configured_count}/{total_count})")
            if status['missing']:
                print(f"   缺失: {', '.join(status['missing'])}")
    
    # 检查连接状态
    print("\n🔗 连接状态检查:")
    
    # 数据库连接
    if check_database_connection():
        print("✅ 数据库配置: 已配置")
    else:
        print("❌ 数据库配置: 未配置或配置错误")
    
    # Redis连接
    if check_redis_connection():
        print("✅ Redis配置: 已配置")
    else:
        print("❌ Redis配置: 未配置或配置错误")
    
    # Weaviate连接
    weaviate_ok, weaviate_msg = check_weaviate_connection()
    if weaviate_ok:
        print("✅ Weaviate连接: 正常")
    else:
        print(f"⚠️  Weaviate连接: {weaviate_msg}")
    
    # 总结
    print("\n📊 配置总结:")
    if missing_required:
        print("❌ 配置不完整，请先配置必需参数")
        sys.exit(1)
    else:
        print("✅ 基本配置完整，服务可以启动")
        
        # 检查重要功能配置
        important_configs = [
            'WEAVIATE_URL', 'WEAVIATE_API_KEY',  # 知识库功能
            'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'MOONSHOT_API_KEY', 'DEEPSEEK_API_KEY',  # AI对话功能
            'COS_REGION', 'COS_BUCKET', 'COS_SECRET_ID', 'COS_SECRET_KEY',  # 文件存储功能
        ]
        
        important_configured = sum(1 for config in important_configs if os.getenv(config))
        important_total = len(important_configs)
        
        if important_configured > 0:
            print(f"🟡 重要功能配置: {important_configured}/{important_total} 已配置")
            print("   建议根据实际需求配置更多功能参数")
        else:
            print("⚠️  重要功能配置: 未配置任何高级功能")
            print("   建议配置语言模型API密钥以启用AI对话功能")

if __name__ == "__main__":
    main()