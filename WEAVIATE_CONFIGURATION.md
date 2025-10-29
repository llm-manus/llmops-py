# Weaviate向量数据库配置说明

## 概述

LLMOps项目支持两种向量数据库方案：
1. **Weaviate云服务** - 用于生产环境的高性能向量搜索
2. **FAISS本地存储** - 默认方案，无需额外配置

## 是否需要启动Weaviate？

**答案：不是必需的，但建议根据使用场景选择**

### 使用场景分析

#### 1. 基础功能（不需要Weaviate）
- ✅ 应用创建和管理
- ✅ 用户认证和授权
- ✅ 基础对话功能
- ✅ 工作流管理
- ✅ API工具集成

#### 2. 知识库功能（需要向量数据库）
- ❌ 文档上传和分段
- ❌ 语义搜索
- ❌ 知识库检索
- ❌ 文档问答

## 配置方案

### 方案1：使用FAISS（默认，推荐用于开发/测试）

**优点**：
- 无需额外配置
- 无需外部依赖
- 适合开发和测试环境
- 数据存储在本地

**缺点**：
- 性能相对较低
- 不支持分布式部署
- 数据不持久化（重启后丢失）

**配置**：
```bash
# 无需任何配置，系统自动使用FAISS
# 向量数据存储在：/opt/llmops/internal/core/vector_store/
```

### 方案2：使用Weaviate云服务（推荐用于生产环境）

**优点**：
- 高性能向量搜索
- 支持大规模数据
- 数据持久化
- 支持分布式部署
- 提供RESTful API

**缺点**：
- 需要额外配置
- 需要网络连接
- 可能有费用成本

**配置步骤**：

1. **注册Weaviate云服务**
   ```bash
   # 访问：https://console.weaviate.cloud/
   # 创建账号并登录
   ```

2. **创建集群**
   ```bash
   # 在控制台中创建新的Weaviate集群
   # 记录集群URL和API密钥
   ```

3. **设置环境变量**
   ```bash
   export WEAVIATE_URL="https://your-cluster.weaviate.network"
   export WEAVIATE_API_KEY="your_api_key_here"
   ```

4. **更新GitHub Secrets**（如果使用自动部署）
   ```bash
   # 在GitHub仓库设置中添加：
   # WEAVIATE_URL: https://your-cluster.weaviate.network
   # WEAVIATE_API_KEY: your_api_key_here
   ```

## 功能影响分析

### 不使用Weaviate的影响

| 功能模块 | 影响程度 | 说明 |
|---------|---------|------|
| 应用管理 | ✅ 无影响 | 完全正常 |
| 用户认证 | ✅ 无影响 | 完全正常 |
| 基础对话 | ✅ 无影响 | 完全正常 |
| 工作流 | ✅ 无影响 | 完全正常 |
| API工具 | ✅ 无影响 | 完全正常 |
| 知识库上传 | ❌ 不可用 | 需要向量数据库 |
| 文档搜索 | ❌ 不可用 | 需要向量数据库 |
| 语义检索 | ❌ 不可用 | 需要向量数据库 |

### 使用Weaviate的好处

1. **完整的知识库功能**
   - 文档上传和分段
   - 语义搜索和检索
   - 智能问答

2. **更好的性能**
   - 更快的向量搜索速度
   - 支持大规模文档库
   - 更好的并发处理能力

3. **生产环境就绪**
   - 数据持久化
   - 高可用性
   - 可扩展性

## 部署建议

### 开发环境
```bash
# 使用FAISS，无需额外配置
# 适合快速开发和测试
```

### 测试环境
```bash
# 可以选择FAISS或Weaviate
# 如果测试知识库功能，建议使用Weaviate
```

### 生产环境
```bash
# 强烈建议使用Weaviate
# 确保知识库功能的完整性和性能
```

## 故障排除

### 常见问题

1. **Weaviate连接失败**
   ```bash
   # 检查网络连接
   curl -I https://your-cluster.weaviate.network
   
   # 检查API密钥
   echo $WEAVIATE_API_KEY
   ```

2. **向量搜索功能不可用**
   ```bash
   # 检查健康状态
   curl http://localhost:5000/health
   
   # 查看weaviate状态
   # 如果显示"not_configured"，说明未配置Weaviate
   # 如果显示"connection_failed"，说明连接失败
   ```

3. **FAISS数据丢失**
   ```bash
   # FAISS数据存储在内存中，重启后会丢失
   # 这是正常现象，如需持久化请使用Weaviate
   ```

## 总结

- **如果只需要基础功能**：无需配置Weaviate，使用默认的FAISS即可
- **如果需要知识库功能**：必须配置Weaviate或使用FAISS（功能有限）
- **生产环境**：强烈建议使用Weaviate云服务
- **开发测试**：可以使用FAISS，配置简单

根据你的具体需求选择合适的方案即可。