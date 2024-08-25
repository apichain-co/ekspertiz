from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37d43130e4d3'
down_revision = '8fe4b2fb63db'
branch_labels = None
depends_on = None


def upgrade():
    # Remove any unnecessary drop table commands
    # op.drop_table('_alembic_tmp_report')  # Only if this table is not needed

    # Only add new columns if they don't already exist
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_by', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('registration_document_seen', sa.Boolean(), nullable=False))
        batch_op.create_foreign_key('fk_report_created_by_staff', 'staff', ['created_by'], ['id'])

    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('branch_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_staff_branch_id', 'branch', ['branch_id'], ['id'])


def downgrade():
    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.drop_constraint('fk_staff_branch_id', type_='foreignkey')
        batch_op.drop_column('branch_id')
        batch_op.drop_column('role')

    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.drop_constraint('fk_report_created_by_staff', type_='foreignkey')
        batch_op.drop_column('registration_document_seen')
        batch_op.drop_column('created_by')
