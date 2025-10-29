# LLMOps服务部署指南

## 概述

本指南详细说明了如何使用GitHub Actions自动部署LLMOps服务到指定服务器。优化后的工作流支持代码检查、构建、部署和启动服务的完整流程。

## 功能特性

- ✅ 代码质量检查（flake8语法检查、代码复杂度分析）
- ✅ 自动测试执行
- ✅ 服务构建和打包
- ✅ 自动部署到目标服务器
- ✅ 数据库迁移
- ✅ 服务启动和健康检查
- ✅ 服务监控和日志管理

## 前置条件

### 1. GitHub仓库配置

在GitHub仓库的Settings > Secrets and variables > Actions中添加以下密钥：

#### 必需配置
- `DEPLOY_HOST`: 目标服务器IP地址或域名
- `DEPLOY_USER`: 服务器用户名
- `DEPLOY_SSH_KEY`: 服务器SSH私钥

#### 可选配置
- `DEPLOY_PORT`: SSH端口（默认22）
- `WEAVIATE_URL`: Weaviate向量数据库URL（用于向量搜索功能）
- `WEAVIATE_API_KEY`: Weaviate API密钥
- `JWT_SECRET_KEY`: JWT签名密钥（**必需**，用于用户认证）
- `COS_REGION`: 腾讯云COS区域（可选，用于文件存储）
- `COS_BUCKET`: 腾讯云COS存储桶（可选）
- `COS_SECRET_ID`: 腾讯云COS访问密钥ID（可选）
- `COS_SECRET_KEY`: 腾讯云COS访问密钥（可选）
- `GITHUB_CLIENT_ID`: GitHub OAuth客户端ID（可选）
- `GITHUB_CLIENT_SECRET`: GitHub OAuth客户端密钥（可选）
- `GITHUB_REDIRECT_URI`: GitHub OAuth回调URI（可选）
- `OPENAI_API_KEY`: OpenAI API密钥（可选）
- `ANTHROPIC_API_KEY`: Anthropic API密钥（可选）
- `MOONSHOT_API_KEY`: 月之暗面API密钥（可选）
- `DEEPSEEK_API_KEY`: DeepSeek API密钥（可选）
- `GAODE_API_KEY`: 高德地图API密钥（可选）
- `SERPER_API_KEY`: Google Serper API密钥（可选）
- `GOOGLE_API_KEY`: Google API密钥（可选）

### 2. 目标服务器配置

#### 系统要求
- Ubuntu 18.04+ 或 CentOS 7+
- Python 3.10
- 至少2GB内存
- 至少10GB磁盘空间

#### 必需软件
```bash
# 安装Python 3.10
sudo apt update
sudo apt install python3.10 python3.10-pip python3.10-venv

# 安装系统依赖
sudo apt install curl tar gzip

# 创建服务用户
sudo useradd -r -s /bin/false www-data
```

#### 环境变量配置

在目标服务器上创建环境变量配置文件：

```bash
# 创建环境变量文件
sudo nano /etc/llmops.env
```

添加以下环境变量（根据实际情况修改）：

```bash
# 数据库配置
export SQLALCHEMY_DATABASE_URI="mysql+pymysql://username:password@localhost:3306/llmops"
export SQLALCHEMY_POOL_SIZE=30
export SQLALCHEMY_POOL_RECYCLE=3600
export SQLALCHEMY_ECHO=True

# JWT认证配置（必需）
export JWT_SECRET_KEY="your_jwt_secret_key_here"

# Redis配置
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_USERNAME=""
export REDIS_PASSWORD="your_redis_password"
export REDIS_DB=0
export REDIS_USE_SSL=False

# Celery配置
export CELERY_BROKER_DB=1
export CELERY_RESULT_BACKEND_DB=1
export CELERY_TASK_IGNORE_RESULT=False
export CELERY_RESULT_EXPIRES=3600
export CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True

# Weaviate向量数据库配置（可选，用于向量搜索功能）
export WEAVIATE_URL="https://your-cluster.weaviate.network"
export WEAVIATE_API_KEY="your_weaviate_api_key"

# 腾讯云COS配置（可选，用于文件存储）
export COS_REGION="ap-beijing"
export COS_BUCKET="your-bucket-name"
export COS_SECRET_ID="your_cos_secret_id"
export COS_SECRET_KEY="your_cos_secret_key"
export COS_SCHEME="https"
export COS_DOMAIN="your-custom-domain.com"

# GitHub OAuth配置（可选，用于第三方登录）
export GITHUB_CLIENT_ID="your_github_client_id"
export GITHUB_CLIENT_SECRET="your_github_client_secret"
export GITHUB_REDIRECT_URI="http://localhost:5000/oauth/authorize/github"

# 语言模型API密钥（可选，用于AI对话功能）
export OPENAI_API_KEY="your_openai_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"
export MOONSHOT_API_KEY="your_moonshot_api_key"
export DEEPSEEK_API_KEY="your_deepseek_api_key"

# 内置工具API密钥（可选，用于特定工具功能）
export GAODE_API_KEY="your_gaode_api_key"
export SERPER_API_KEY="your_serper_api_key"
export GOOGLE_API_KEY="your_google_api_key"

# 其他配置
export ASSISTANT_AGENT_ID="6774fcef-b594-8008-b30c-a05b8190afe6"
export WTF_CSRF_ENABLED=False
export FLASK_APP=app.http.app
export FLASK_ENV=production
```

### 3. 数据库配置

#### MySQL数据库设置
```sql
-- 创建数据库
CREATE DATABASE llmops CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户
CREATE USER 'llmops'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON llmops.* TO 'llmops'@'localhost';
FLUSH PRIVILEGES;
```

#### Redis配置
```bash
# 安装Redis
sudo apt install redis-server

# 配置Redis密码
sudo nano /etc/redis/redis.conf
# 取消注释并设置：requirepass your_redis_password

# 重启Redis
sudo systemctl restart redis-server
```

#### 配置优先级说明

**🔴 必需配置（影响核心功能）**
- `JWT_SECRET_KEY` - 用户认证，不配置无法登录
- `SQLALCHEMY_DATABASE_URI` - 数据库连接，不配置无法启动
- `REDIS_HOST` - 缓存和任务队列，不配置功能受限

**🟡 建议配置（影响重要功能）**
- `WEAVIATE_URL` + `WEAVIATE_API_KEY` - 知识库功能
- `OPENAI_API_KEY` 等语言模型密钥 - AI对话功能
- `COS_*` 配置 - 文件上传功能

**🟢 可选配置（影响特定功能）**
- `GITHUB_*` 配置 - 第三方登录
- `GAODE_API_KEY` 等工具密钥 - 特定工具功能

#### Weaviate向量数据库配置（可选）

LLMOps项目支持两种向量数据库：
1. **Weaviate云服务**（推荐用于生产环境）
2. **FAISS本地存储**（默认，无需额外配置）

##### 选项1：使用Weaviate云服务
```bash
# 1. 注册Weaviate云服务账号
# 访问：https://console.weaviate.cloud/

# 2. 创建集群并获取连接信息
# - 集群URL: https://your-cluster.weaviate.network
# - API密钥: 在控制台中生成

# 3. 设置环境变量
export WEAVIATE_URL="https://your-cluster.weaviate.network"
export WEAVIATE_API_KEY="your_api_key_here"
```

##### 选项2：使用FAISS本地存储（默认）
```bash
# 无需额外配置，系统会自动使用FAISS
# 向量数据存储在：/opt/llmops/internal/core/vector_store/
```

**注意**：
- 如果配置了Weaviate，系统会优先使用Weaviate进行向量搜索
- 如果未配置Weaviate，系统会使用FAISS本地存储
- 向量搜索功能主要用于知识库检索和文档搜索

## 部署流程

### 1. 自动部署

当代码推送到main或master分支时，GitHub Actions会自动执行以下步骤：

1. **代码质量检查**
   - Python语法检查
   - 代码风格检查
   - 代码复杂度分析
   - 自动测试执行

2. **构建和打包**
   - 安装依赖
   - 创建部署包
   - 生成启动脚本
   - 创建systemd服务文件

3. **部署到服务器**
   - 停止现有服务
   - 备份当前部署
   - 上传新部署包
   - 解压和配置

4. **服务启动**
   - 安装Python依赖
   - 运行数据库迁移
   - 启动服务
   - 健康检查

### 2. 手动部署

可以通过GitHub Actions页面手动触发部署：

1. 进入GitHub仓库的Actions页面
2. 选择"LLMOps Service Deployment"工作流
3. 点击"Run workflow"按钮
4. 选择分支并点击"Run workflow"

## 服务管理

### 服务控制命令

```bash
# 启动服务
sudo systemctl start llmops

# 停止服务
sudo systemctl stop llmops

# 重启服务
sudo systemctl restart llmops

# 查看服务状态
sudo systemctl status llmops

# 查看服务日志
sudo journalctl -u llmops -f

# 查看最近100行日志
sudo journalctl -u llmops -n 100
```

### 健康检查

服务提供以下健康检查端点：

- `GET /ping` - 基础连通性检查
- `GET /health` - 详细健康状态检查

健康检查响应示例：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "status": "healthy",
    "service": "LLMOps",
    "version": "1.0.0",
    "database": "connected",
    "redis": "connected",
    "timestamp": "unique-timestamp"
  }
}
```

## 故障排除

### 常见问题

1. **服务启动失败**
   ```bash
   # 查看详细日志
   sudo journalctl -u llmops --no-pager -l
   
   # 检查环境变量
   sudo systemctl show-environment
   ```

2. **数据库连接失败**
   - 检查数据库服务是否运行
   - 验证连接字符串是否正确
   - 确认数据库用户权限

3. **Redis连接失败**
   - 检查Redis服务状态
   - 验证密码配置
   - 确认网络连通性

4. **端口占用**
   ```bash
   # 检查端口占用
   sudo netstat -tlnp | grep :5000
   
   # 杀死占用进程
   sudo kill -9 <PID>
   ```

### 日志位置

- 服务日志：`sudo journalctl -u llmops`
- 应用日志：`/opt/llmops/logs/`（如果配置了文件日志）
- 系统日志：`/var/log/syslog`

## 安全注意事项

1. **SSH密钥安全**
   - 使用强密码保护SSH私钥
   - 定期轮换SSH密钥
   - 限制SSH访问IP范围

2. **环境变量安全**
   - 不要在代码中硬编码敏感信息
   - 使用环境变量或密钥管理系统
   - 定期更新密码和密钥

3. **网络安全**
   - 配置防火墙规则
   - 使用HTTPS（推荐）
   - 限制数据库和Redis的访问范围

## 监控和维护

### 性能监控

建议配置以下监控：

1. **服务状态监控**
   - 定期检查健康检查端点
   - 监控服务进程状态
   - 设置告警机制

2. **资源监控**
   - CPU使用率
   - 内存使用率
   - 磁盘空间
   - 网络流量

3. **应用监控**
   - 请求响应时间
   - 错误率
   - 数据库连接池状态

### 定期维护

1. **日志清理**
   ```bash
   # 清理旧日志
   sudo journalctl --vacuum-time=30d
   ```

2. **数据库维护**
   - 定期备份数据库
   - 优化数据库性能
   - 清理过期数据

3. **系统更新**
   - 定期更新系统包
   - 更新Python依赖
   - 应用安全补丁

## 回滚操作

如果需要回滚到之前的版本：

```bash
# 停止当前服务
sudo systemctl stop llmops

# 恢复备份
sudo mv /opt/llmops.backup.YYYYMMDD_HHMMSS /opt/llmops

# 重启服务
sudo systemctl start llmops
```

## 支持

如果遇到问题，请：

1. 查看本文档的故障排除部分
2. 检查GitHub Actions的部署日志
3. 查看目标服务器的服务日志
4. 联系技术支持团队

---

**注意**: 本部署指南基于当前的项目结构编写。如果项目结构发生变化，可能需要相应调整部署配置。