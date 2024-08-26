from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64da40ae4e4f'
down_revision = 'f4a4cd3e3e57'
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table with the updated schema (without NOT NULL constraint on status)
    op.create_table(
        'expertise_feature_new',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('feature_name', sa.String(length=50), nullable=False),
        sa.Column('status', sa.Integer(), nullable=True),  # Updated to allow NULLs
        # Add other columns as required
    )

    # Copy data from the old table to the new table
    op.execute('''
        INSERT INTO expertise_feature_new (id, feature_name, status)
        SELECT id, feature_name, status FROM expertise_feature
    ''')

    # Drop the old table
    op.drop_table('expertise_feature')

    # Rename the new table to the old table's name
    op.rename_table('expertise_feature_new', 'expertise_feature')


def downgrade():
    # Recreate the old table with the original schema (with NOT NULL constraint on status)
    op.create_table(
        'expertise_feature_old',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('feature_name', sa.String(length=50), nullable=False),
        sa.Column('status', sa.Integer(), nullable=False),  # NOT NULL constraint restored
        # Add other columns as required
    )

    # Copy data back from the new table to the old table
    op.execute('''
        INSERT INTO expertise_feature_old (id, feature_name, status)
        SELECT id, feature_name, status FROM expertise_feature
    ''')

    # Drop the current table
    op.drop_table('expertise_feature')

    # Rename the old table back to its original name
    op.rename_table('expertise_feature_old', 'expertise_feature')
