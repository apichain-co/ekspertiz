from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4a4cd3e3e57'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Use batch mode to safely alter the table in SQLite
    with op.batch_alter_table('expertise_report', schema=None) as batch_op:
        # Drop the package_expertise_id column, which will also drop the associated foreign key constraint
        batch_op.drop_column('package_expertise_id')


def downgrade():
    # Re-add the package_expertise_id column and the foreign key constraint in case of a downgrade
    with op.batch_alter_table('expertise_report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('package_expertise_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key(None, 'package_expertise', ['package_expertise_id'], ['id'])
