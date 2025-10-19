#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/22 00:02
#Author  :Emcikem
@File    :conversation.py
"""
from datetime import datetime
import uuid
from sqlalchemy import (
    Column,
    UUID,
    String,
    Text,
    DateTime,
    PrimaryKeyConstraint,
    Index,
    text, Boolean, JSON, Integer, Numeric, Float, func, asc,
)
from sqlalchemy.orm import relationship

from internal.extension.database_extension import db

class Conversation(db.Model):
    """交流会话模型"""
    __tablename__ = "conversation"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_conversation_id"),
    )

    id = Column(String(36), nullable=False, default=uuid.uuid4)
    app_id = Column(String(36), nullable=False)
    name = Column(String(255), nullable=False, default="")
    summary = Column(Text, nullable=False, default="")
    is_pinned = Column(Boolean, nullable=False, default=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    invoke_from = Column(String(255), nullable=False, default="")
    created_by = Column(String(36), nullable=False, default="") # 会话创建者，会随着invoke_from的差异记录不同的信息，其中web_app和debugger会记录账号id、service_api会记录终端用户id
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    @property
    def is_new(self) -> bool:
        """只读属性，用于判断该会话是否是第一次创建"""
        message_count = db.session.query(func.count(Message.id)).filter(
            Message.conversation_id == self.id
        ).scalar()

        return False if message_count > 1 else True


class Message(db.Model):
    """交流消息模型"""
    __tablename__ = "message"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_message_id"),
    )

    id = Column(String(36), nullable=False, default=uuid.uuid4)
    app_id = Column(String(36), nullable=False)
    conversation_id = Column(String(36), nullable=False)
    invoke_from = Column(String(255), nullable=False, default="")
    created_by = Column(String(36), nullable=False, default="")

    # 消息关联的原始问题
    query = Column(Text, nullable=False, default="")
    image_urls = Column(JSON, nullable=False, default=[])
    message = Column(JSON, nullable=False, default="")
    message_token_count = Column(Integer, nullable=False, default=0)
    message_unit_price = Column(Numeric(10, 7), nullable=False, default=0)
    message_price_unit = Column(Numeric(10, 4), nullable=False, default=0)

    # 消息关联的答案信息
    answer = Column(Text, nullable=False, default="")
    answer_token_count = Column(Integer, nullable=False, default=0)
    answer_unit_price = Column(Numeric(10, 7), nullable=False, default=0)
    answer_price_unit = Column(Numeric(10, 4), nullable=False, default=0)

    # 消息的相关统计信息
    latency = Column(Float, nullable=False, default=0.0)
    is_deleted = Column(Boolean, nullable=False, default=False)
    status = Column(String(255), nullable=False, default="")
    error = Column(Text, nullable=False, default="")
    total_token_count = Column(Integer, nullable=False, default=0)
    total_price = Column(Numeric(10, 7), nullable=False, default=0)

    # 消息时间相关信息
    updated_at = Column(DateTime, default=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    # 智能体推理列表，创建表关联
    agent_thoughts = relationship(
        "MessageAgentThought",
        backref="msg",
        lazy="selectin",
        passive_deletes="all",
        uselist=True,
        foreign_keys=[id],
        primaryjoin="MessageAgentThought.message_id == Message.id",

    )

class MessageAgentThought(db.Model):
    """消息智能体观察表，用于记录Agent生成最终消息答案时"""
    __tablename__ = "message_agent_thought"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_message_agent_thought_id"),
    )
    id = Column(String(36), nullable=False, default=uuid.uuid4)

    # 推理步骤相关信息
    app_id = Column(String(36), nullable=False)
    conversation_id = Column(String(36), nullable=False)
    message_id = Column(String(36), nullable=False)
    invoke_from = Column(String(255), nullable=False, default="")
    created_by = Column(String(36), nullable=False, default="")

    # 该步骤在消息中执行的位置
    position = Column(Integer, nullable=False, default=0)

    # 推理与观察，分别记录LLM和非LLM产生的消息
    event = Column(String(255), nullable=False, default="")
    thought = Column(Text, nullable=False, default="")
    observation = Column(Text, nullable=False, default="")

    # 根据相关，涵盖工具名称，输入，在调用工具时会生成
    tool = Column(Text, nullable=False, default="")
    tool_input = Column(JSON, nullable=False, default="")


    # Agent推理观察步骤使用的消息列表（传递prompt消息内容）
    message = Column(JSON, nullable=False, default="")
    message_token_count = Column(Integer, nullable=False, default=0)
    message_unit_price = Column(Numeric(10, 7), nullable=False, default=0)
    message_price_unit = Column(Numeric(10, 4), nullable=False, default=0)

    # LLM生成内容相关
    answer = Column(Text, nullable=False, default="")
    answer_token_count = Column(Integer, nullable=False, default=0)
    answer_unit_price = Column(Numeric(10, 7), nullable=False, default=0)
    answer_price_unit = Column(Numeric(10, 4), nullable=False, default=0)

    # Agent推理观察统计相关
    total_token_count = Column(Integer, nullable=False, default=0)
    total_price = Column(Numeric(10, 7), nullable=False, default=0)
    latency = Column(Float, nullable=False, default=0.0)

    # 时间相关信息
    updated_at = Column(DateTime, default=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
