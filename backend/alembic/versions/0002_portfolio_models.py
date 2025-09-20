"""Add portfolio content models

Revision ID: 0002_portfolio_models
Revises: 0001_initial_baseline
Create Date: 2025-09-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002_portfolio_models'
down_revision = '0001_initial_baseline'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create profile_info table
    op.create_table('profile_info',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('subtitle', sa.Text(), nullable=True),
        sa.Column('bio_description', sa.Text(), nullable=False),
        sa.Column('years_experience', sa.Integer(), nullable=False),
        sa.Column('availability_status', sa.String(length=100), nullable=False),
        sa.Column('resume_url', sa.String(length=500), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('linkedin_url', sa.String(length=500), nullable=True),
        sa.Column('github_url', sa.String(length=500), nullable=True),
        sa.Column('portfolio_url', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profile_info_id'), 'profile_info', ['id'], unique=False)

    # Create profile_stats table
    op.create_table('profile_stats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('metric_name', sa.String(length=255), nullable=False),
        sa.Column('metric_value', sa.String(length=100), nullable=False),
        sa.Column('metric_description', sa.String(length=255), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profile_stats_id'), 'profile_stats', ['id'], unique=False)

    # Create skills table
    op.create_table('skills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('icon_name', sa.String(length=100), nullable=True),
        sa.Column('color_gradient', sa.String(length=255), nullable=True),
        sa.Column('projects_count', sa.String(length=100), nullable=True),
        sa.Column('impact_metric', sa.String(length=255), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('skill_level', sa.String(length=50), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('is_featured', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_skills_id'), 'skills', ['id'], unique=False)

    # Create project_categories table
    op.create_table('project_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon_name', sa.String(length=100), nullable=True),
        sa.Column('color_theme', sa.String(length=100), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_project_categories_id'), 'project_categories', ['id'], unique=False)

    # Create projects table
    op.create_table('projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('short_description', sa.Text(), nullable=False),
        sa.Column('full_description', sa.Text(), nullable=True),
        sa.Column('impact_metric', sa.String(length=255), nullable=True),
        sa.Column('business_problem', sa.Text(), nullable=True),
        sa.Column('solution_approach', sa.Text(), nullable=True),
        sa.Column('results_achieved', sa.Text(), nullable=True),
        sa.Column('technologies', sa.JSON(), nullable=True),
        sa.Column('methodology', sa.Text(), nullable=True),
        sa.Column('challenges_overcome', sa.Text(), nullable=True),
        sa.Column('thumbnail_url', sa.String(length=500), nullable=True),
        sa.Column('image_gallery', sa.JSON(), nullable=True),
        sa.Column('demo_url', sa.String(length=500), nullable=True),
        sa.Column('github_url', sa.String(length=500), nullable=True),
        sa.Column('case_study_url', sa.String(length=500), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('is_featured', sa.Boolean(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('project_duration', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['project_categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)

    # Create experience table
    op.create_table('experience',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_name', sa.String(length=255), nullable=False),
        sa.Column('position_title', sa.String(length=255), nullable=False),
        sa.Column('company_description', sa.Text(), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('is_current', sa.Boolean(), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('work_type', sa.String(length=100), nullable=True),
        sa.Column('key_responsibilities', sa.JSON(), nullable=True),
        sa.Column('key_achievements', sa.JSON(), nullable=True),
        sa.Column('technologies_used', sa.JSON(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('is_featured', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_experience_id'), 'experience', ['id'], unique=False)

    # Create testimonials table
    op.create_table('testimonials',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('author_name', sa.String(length=255), nullable=False),
        sa.Column('author_title', sa.String(length=255), nullable=True),
        sa.Column('author_company', sa.String(length=255), nullable=True),
        sa.Column('author_avatar_url', sa.String(length=500), nullable=True),
        sa.Column('testimonial_text', sa.Text(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('project_context', sa.String(length=255), nullable=True),
        sa.Column('collaboration_type', sa.String(length=100), nullable=True),
        sa.Column('is_featured', sa.Boolean(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('is_approved', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_testimonials_id'), 'testimonials', ['id'], unique=False)

    # Create blog_posts table
    op.create_table('blog_posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('excerpt', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('meta_title', sa.String(length=255), nullable=True),
        sa.Column('meta_description', sa.Text(), nullable=True),
        sa.Column('featured_image_url', sa.String(length=500), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_blog_posts_id'), 'blog_posts', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_blog_posts_id'), table_name='blog_posts')
    op.drop_table('blog_posts')
    op.drop_index(op.f('ix_testimonials_id'), table_name='testimonials')
    op.drop_table('testimonials')
    op.drop_index(op.f('ix_experience_id'), table_name='experience')
    op.drop_table('experience')
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_table('projects')
    op.drop_index(op.f('ix_project_categories_id'), table_name='project_categories')
    op.drop_table('project_categories')
    op.drop_index(op.f('ix_skills_id'), table_name='skills')
    op.drop_table('skills')
    op.drop_index(op.f('ix_profile_stats_id'), table_name='profile_stats')
    op.drop_table('profile_stats')
    op.drop_index(op.f('ix_profile_info_id'), table_name='profile_info')
    op.drop_table('profile_info')