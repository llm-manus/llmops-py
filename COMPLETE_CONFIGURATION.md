# LLMOps完整配置参数清单

## 概述

本文档列出了LLMOps项目中所有可配置的环境变量参数，包括已配置和未配置的参数。

## 已配置的参数

### 核心数据库配置
- `SQLALCHEMY_DATABASE_URI` - 数据库连接字符串
- `SQLALCHEMY_POOL_SIZE` - 连接池大小
- `SQLALCHEMY_POOL_RECYCLE` - 连接回收时间
- `SQLALCHEMY_ECHO` - SQL日志输出

### Redis配置
- `REDIS_HOST` - Redis主机地址
- `REDIS_PORT` - Redis端口
- `REDIS_USERNAME` - Redis用户名
- `REDIS_PASSWORD` - Redis密码
- `REDIS_DB` - Redis数据库编号
- `REDIS_USE_SSL` - 是否使用SSL

### Celery配置
- `CELERY_BROKER_DB` - Celery代理数据库
- `CELERY_RESULT_BACKEND_DB` - Celery结果后端数据库
- `CELERY_TASK_IGNORE_RESULT` - 忽略任务结果
- `CELERY_RESULT_EXPIRES` - 结果过期时间
- `CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP` - 启动时重试连接

### 向量数据库配置
- `WEAVIATE_URL` - Weaviate集群URL
- `WEAVIATE_API_KEY` - Weaviate API密钥

### 应用配置
- `ASSISTANT_AGENT_ID` - 辅助Agent应用ID
- `WTF_CSRF_ENABLED` - CSRF保护
- `FLASK_APP` - Flask应用入口
- `FLASK_ENV` - Flask环境

## 缺失的配置参数

### 🔴 必需配置（影响核心功能）

#### JWT认证配置
- `JWT_SECRET_KEY` - JWT签名密钥（**必需**）
  - 用途：用户认证token签名
  - 影响：用户登录、API认证
  - 建议：使用强随机字符串

### 🟡 可选配置（影响特定功能）

#### 腾讯云COS对象存储配置
- `COS_REGION` - COS区域
- `COS_BUCKET` - COS存储桶名称
- `COS_SECRET_ID` - COS访问密钥ID
- `COS_SECRET_KEY` - COS访问密钥
- `COS_SCHEME` - COS协议（默认https）
- `COS_DOMAIN` - COS自定义域名（可选）

#### GitHub OAuth配置
- `GITHUB_CLIENT_ID` - GitHub OAuth客户端ID
- `GITHUB_CLIENT_SECRET` - GitHub OAuth客户端密钥
- `GITHUB_REDIRECT_URI` - GitHub OAuth回调URI

#### 语言模型API密钥配置
- `OPENAI_API_KEY` - OpenAI API密钥
- `ANTHROPIC_API_KEY` - Anthropic API密钥
- `MOONSHOT_API_KEY` - 月之暗面API密钥
- `DEEPSEEK_API_KEY` - DeepSeek API密钥

#### 内置工具API密钥配置
- `GAODE_API_KEY` - 高德地图API密钥
- `SERPER_API_KEY` - Google Serper API密钥
- `GOOGLE_API_KEY` - Google API密钥

## 配置优先级和影响分析

### 🔴 高优先级（必须配置）
1. **JWT_SECRET_KEY** - 影响用户认证，不配置无法登录
2. **数据库配置** - 影响数据存储，不配置无法启动
3. **Redis配置** - 影响缓存和任务队列，不配置功能受限

### 🟡 中优先级（建议配置）
1. **Weaviate配置** - 影响知识库功能
2. **语言模型API密钥** - 影响AI对话功能
3. **COS配置** - 影响文件上传功能

### 🟢 低优先级（可选配置）
1. **OAuth配置** - 影响第三方登录
2. **工具API密钥** - 影响特定工具功能

## 更新配置建议

### 1. 更新.env.example文件
```bash
# ===================
# JWT认证配置（必需）
# ===================
JWT_SECRET_KEY=your_jwt_secret_key_here

# ===================
# 腾讯云COS配置（可选）
# ===================
COS_REGION=ap-beijing
COS_BUCKET=your-bucket-name
COS_SECRET_ID=your_cos_secret_id
COS_SECRET_KEY=your_cos_secret_key
COS_SCHEME=https
COS_DOMAIN=your-custom-domain.com

# ===================
# GitHub OAuth配置（可选）
# ===================
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=http://localhost:5000/oauth/authorize/github

# ===================
# 语言模型API密钥（可选）
# ===================
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
MOONSHOT_API_KEY=your_moonshot_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key

# ===================
# 内置工具API密钥（可选）
# ===================
GAODE_API_KEY=your_gaode_api_key
SERPER_API_KEY=your_serper_api_key
GOOGLE_API_KEY=your_google_api_key
```

### 2. 更新GitHub Action工作流
在`.github/workflows/python-app.yml`中添加：
```yaml
# JWT配置 - 必需
# JWT_SECRET_KEY: ${{ secrets.JWT_SECRET_KEY }}

# COS配置 - 可选
# COS_REGION: ${{ secrets.COS_REGION }}
# COS_BUCKET: ${{ secrets.COS_BUCKET }}
# COS_SECRET_ID: ${{ secrets.COS_SECRET_ID }}
# COS_SECRET_KEY: ${{ secrets.COS_SECRET_KEY }}

# GitHub OAuth配置 - 可选
# GITHUB_CLIENT_ID: ${{ secrets.GITHUB_CLIENT_ID }}
# GITHUB_CLIENT_SECRET: ${{ secrets.GITHUB_CLIENT_SECRET }}
# GITHUB_REDIRECT_URI: ${{ secrets.GITHUB_REDIRECT_URI }}

# 语言模型API密钥 - 可选
# OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
# ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
# MOONSHOT_API_KEY: ${{ secrets.MOONSHOT_API_KEY }}
# DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}

# 工具API密钥 - 可选
# GAODE_API_KEY: ${{ secrets.GAODE_API_KEY }}
# SERPER_API_KEY: ${{ secrets.SERPER_API_KEY }}
# GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
```

### 3. 更新健康检查
在健康检查中添加JWT配置检查：
```python
# 检查JWT配置
jwt_status = "configured" if os.getenv('JWT_SECRET_KEY') else "not_configured"
```

## 功能影响分析

### 不配置JWT_SECRET_KEY的影响
- ❌ 用户无法登录
- ❌ API认证失败
- ❌ 会话管理失效

### 不配置语言模型API密钥的影响
- ❌ AI对话功能不可用
- ❌ 智能问答功能受限
- ❌ 工作流中的LLM节点无法工作

### 不配置COS的影响
- ❌ 文件上传功能不可用
- ❌ 图片存储功能受限

### 不配置OAuth的影响
- ❌ 第三方登录功能不可用
- ✅ 密码登录仍然可用

### 不配置工具API密钥的影响
- ❌ 对应工具功能不可用
- ✅ 其他工具仍然可用

## 建议的配置策略

### 最小化配置（仅核心功能）
```bash
# 必需配置
JWT_SECRET_KEY=your_jwt_secret_key
SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:pass@localhost:3306/llmops
REDIS_HOST=localhost
REDIS_PASSWORD=your_redis_password
```

### 完整配置（所有功能）
```bash
# 包含所有上述配置参数
# 根据实际需求选择性配置
```

## 总结

当前配置中缺失的主要参数：
1. **JWT_SECRET_KEY** - 必需，影响用户认证
2. **各种API密钥** - 可选，影响特定功能
3. **COS配置** - 可选，影响文件存储
4. **OAuth配置** - 可选，影响第三方登录

建议优先配置JWT_SECRET_KEY，其他配置根据实际需求逐步添加。