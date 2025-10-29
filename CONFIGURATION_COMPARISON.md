# LLMOps配置参数对比表

## 配置完整性对比

| 配置类别 | 参数名称 | 当前状态 | 影响功能 | 优先级 | 建议 |
|---------|---------|---------|---------|--------|------|
| **JWT认证** | `JWT_SECRET_KEY` | ❌ 缺失 | 用户认证、API认证 | 🔴 必需 | 立即配置 |
| **数据库** | `SQLALCHEMY_DATABASE_URI` | ✅ 已配置 | 数据存储 | 🔴 必需 | 已配置 |
| **Redis** | `REDIS_HOST` | ✅ 已配置 | 缓存、任务队列 | 🔴 必需 | 已配置 |
| **Weaviate** | `WEAVIATE_URL` | ✅ 已配置 | 向量搜索 | 🟡 建议 | 已配置 |
| **Weaviate** | `WEAVIATE_API_KEY` | ✅ 已配置 | 向量搜索 | 🟡 建议 | 已配置 |
| **COS** | `COS_REGION` | ❌ 缺失 | 文件存储 | 🟡 建议 | 可选配置 |
| **COS** | `COS_BUCKET` | ❌ 缺失 | 文件存储 | 🟡 建议 | 可选配置 |
| **COS** | `COS_SECRET_ID` | ❌ 缺失 | 文件存储 | 🟡 建议 | 可选配置 |
| **COS** | `COS_SECRET_KEY` | ❌ 缺失 | 文件存储 | 🟡 建议 | 可选配置 |
| **GitHub OAuth** | `GITHUB_CLIENT_ID` | ❌ 缺失 | 第三方登录 | 🟢 可选 | 可选配置 |
| **GitHub OAuth** | `GITHUB_CLIENT_SECRET` | ❌ 缺失 | 第三方登录 | 🟢 可选 | 可选配置 |
| **GitHub OAuth** | `GITHUB_REDIRECT_URI` | ❌ 缺失 | 第三方登录 | 🟢 可选 | 可选配置 |
| **OpenAI** | `OPENAI_API_KEY` | ❌ 缺失 | AI对话 | 🟡 建议 | 可选配置 |
| **Anthropic** | `ANTHROPIC_API_KEY` | ❌ 缺失 | AI对话 | 🟡 建议 | 可选配置 |
| **月之暗面** | `MOONSHOT_API_KEY` | ❌ 缺失 | AI对话 | 🟡 建议 | 可选配置 |
| **DeepSeek** | `DEEPSEEK_API_KEY` | ❌ 缺失 | AI对话 | 🟡 建议 | 可选配置 |
| **高德地图** | `GAODE_API_KEY` | ❌ 缺失 | 天气查询 | 🟢 可选 | 可选配置 |
| **Google搜索** | `SERPER_API_KEY` | ❌ 缺失 | 网络搜索 | 🟢 可选 | 可选配置 |
| **Google API** | `GOOGLE_API_KEY` | ❌ 缺失 | Google工具 | 🟢 可选 | 可选配置 |

## 功能影响分析

### 🔴 核心功能（必需配置）
- **用户认证**: 需要 `JWT_SECRET_KEY`
- **数据存储**: 需要 `SQLALCHEMY_DATABASE_URI`
- **缓存和任务**: 需要 `REDIS_HOST`

### 🟡 重要功能（建议配置）
- **知识库搜索**: 需要 `WEAVIATE_URL` + `WEAVIATE_API_KEY`
- **AI对话**: 需要语言模型API密钥（`OPENAI_API_KEY` 等）
- **文件存储**: 需要COS配置（`COS_REGION` 等）

### 🟢 扩展功能（可选配置）
- **第三方登录**: 需要OAuth配置（`GITHUB_CLIENT_ID` 等）
- **特定工具**: 需要工具API密钥（`GAODE_API_KEY` 等）

## 配置建议

### 最小化配置（仅核心功能）
```bash
# 必需配置
JWT_SECRET_KEY=your_jwt_secret_key
SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:pass@localhost:3306/llmops
REDIS_HOST=localhost
REDIS_PASSWORD=your_redis_password
```

### 标准配置（核心 + 重要功能）
```bash
# 包含上述配置 +
WEAVIATE_URL=https://your-cluster.weaviate.network
WEAVIATE_API_KEY=your_weaviate_api_key
OPENAI_API_KEY=your_openai_api_key
COS_REGION=ap-beijing
COS_BUCKET=your-bucket-name
COS_SECRET_ID=your_cos_secret_id
COS_SECRET_KEY=your_cos_secret_key
```

### 完整配置（所有功能）
```bash
# 包含所有上述配置 +
ANTHROPIC_API_KEY=your_anthropic_api_key
MOONSHOT_API_KEY=your_moonshot_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=http://localhost:5000/oauth/authorize/github
GAODE_API_KEY=your_gaode_api_key
SERPER_API_KEY=your_serper_api_key
GOOGLE_API_KEY=your_google_api_key
```

## 配置检查工具

使用提供的 `check_config.py` 脚本检查配置：

```bash
python check_config.py
```

该脚本会：
1. 检查必需配置是否完整
2. 显示可选配置的配置状态
3. 测试数据库和Redis连接
4. 测试Weaviate连接（如果配置）
5. 提供配置建议

## 总结

当前配置状态：
- ✅ **核心功能**: 数据库和Redis已配置
- ❌ **认证功能**: 缺少JWT密钥（**必须立即配置**）
- ✅ **向量搜索**: Weaviate已配置
- ❌ **AI对话**: 缺少语言模型API密钥
- ❌ **文件存储**: 缺少COS配置
- ❌ **扩展功能**: 缺少OAuth和工具API密钥

**建议优先级**：
1. 🔴 **立即配置**: `JWT_SECRET_KEY`
2. 🟡 **建议配置**: 语言模型API密钥（如 `OPENAI_API_KEY`）
3. 🟡 **可选配置**: COS配置（如果需要文件存储）
4. 🟢 **按需配置**: 其他功能配置