from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04ba5db02453'
down_revision = '64da40ae4e4f'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the new table if it exists (safety measure)
    op.execute('DROP TABLE IF EXISTS expertise_feature_new')

    # Create a new table with the desired schema (with status nullable)
    op.create_table(
        'expertise_feature_new',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True),  # Making status nullable
        sa.Column('expertise_report_id', sa.Integer(), nullable=False),
    )

    # Copy data from the old table to the new table
    op.execute('''
        INSERT INTO expertise_feature_new (id, name, status, expertise_report_id)
        SELECT id, name, status, expertise_report_id FROM expertise_feature
    ''')

    # Drop the old table
    op.drop_table('expertise_feature')

    # Rename the new table to the old table's name
    op.rename_table('expertise_feature_new', 'expertise_feature')


def downgrade():
    # Drop the new table if it exists (safety measure)
    op.execute('DROP TABLE IF EXISTS expertise_feature_old')

    # Recreate the old table with the original schema (with status not nullable)
    op.create_table(
        'expertise_feature_old',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),  # Reverting to NOT NULL
        sa.Column('expertise_report_id', sa.Integer(), nullable=False),
    )

    # Copy data back from the new table to the old table
    op.execute('''
        INSERT INTO expertise_feature_old (id, name, status, expertise_report_id)
        SELECT id, name, status, expertise_report_id FROM expertise_feature
    ''')

    # Drop the current table
    op.drop_table('expertise_feature')

    # Rename the old table back to its original name
    op.rename_table('expertise_feature_old', 'expertise_feature')
