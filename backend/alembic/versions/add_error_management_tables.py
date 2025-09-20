"""Add error management tables

Revision ID: add_error_management_tables
Revises: 
Create Date: 2025-09-20 13:47:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_error_management_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create error severity enum
    error_severity = postgresql.ENUM(
        'critical', 'high', 'medium', 'low', 'info',
        name='errorseverity'
    )
    error_severity.create(op.get_bind(), checkfirst=True)
    
    # Create error category enum
    error_category = postgresql.ENUM(
        'system', 'business_logic', 'user_input', 'external_service', 'security',
        name='errorcategory'
    )
    error_category.create(op.get_bind(), checkfirst=True)
    
    # Create error source enum
    error_source = postgresql.ENUM(
        'frontend', 'backend', 'database', 'external_api', 'system',
        name='errorsource'
    )
    error_source.create(op.get_bind(), checkfirst=True)
    
    # Create error_records table
    op.create_table('error_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('severity', error_severity, nullable=False),
        sa.Column('category', error_category, nullable=False),
        sa.Column('source', error_source, nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('error_type', sa.String(length=255), nullable=True),
        sa.Column('stack_trace', sa.Text(), nullable=True),
        sa.Column('context', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('request_id', sa.String(length=255), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('session_id', sa.String(length=255), nullable=True),
        sa.Column('url', sa.String(length=2048), nullable=True),
        sa.Column('method', sa.String(length=10), nullable=True),
        sa.Column('status_code', sa.Integer(), nullable=True),
        sa.Column('resolved', sa.Boolean(), nullable=False, default=False),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('resolved_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('occurrence_count', sa.Integer(), nullable=False, default=1),
        sa.Column('first_occurrence', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_occurrence', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_error_records_request_id'), 'error_records', ['request_id'], unique=False)
    op.create_index(op.f('ix_error_records_user_id'), 'error_records', ['user_id'], unique=False)
    op.create_index(op.f('ix_error_records_timestamp'), 'error_records', ['timestamp'], unique=False)
    op.create_index(op.f('ix_error_records_severity'), 'error_records', ['severity'], unique=False)
    op.create_index(op.f('ix_error_records_resolved'), 'error_records', ['resolved'], unique=False)
    
    # Create system_cleanup_logs table
    op.create_table('system_cleanup_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('cleanup_type', sa.String(length=100), nullable=False),
        sa.Column('operation', sa.String(length=100), nullable=False),
        sa.Column('files_processed', sa.Integer(), nullable=False, default=0),
        sa.Column('files_affected', sa.Integer(), nullable=False, default=0),
        sa.Column('bytes_processed', sa.Integer(), nullable=False, default=0),
        sa.Column('success', sa.Boolean(), nullable=False, default=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('details', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for cleanup logs
    op.create_index(op.f('ix_system_cleanup_logs_timestamp'), 'system_cleanup_logs', ['timestamp'], unique=False)
    op.create_index(op.f('ix_system_cleanup_logs_cleanup_type'), 'system_cleanup_logs', ['cleanup_type'], unique=False)
    op.create_index(op.f('ix_system_cleanup_logs_success'), 'system_cleanup_logs', ['success'], unique=False)


def downgrade():
    # Drop tables
    op.drop_table('system_cleanup_logs')
    op.drop_table('error_records')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS errorsource')
    op.execute('DROP TYPE IF EXISTS errorcategory')
    op.execute('DROP TYPE IF EXISTS errorseverity')