"""migration done

Revision ID: 849b21212420
Revises: 3f7bf0ae8877
Create Date: 2024-08-30 01:02:20.397198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '849b21212420'
down_revision = '3f7bf0ae8877'
branch_labels = None
depends_on = None


def upgrade():
    # Use batch mode for SQLite-compatible migration
    with op.batch_alter_table('report', schema=None) as batch_op:
        # Only add columns if they don't already exist
        # Assuming columns 'vehicle_id', 'customer_id', 'package_id', etc., already exist, we skip adding them again.

        # Create foreign key constraints (if they don't exist)
        batch_op.create_foreign_key('fk_report_package_id', 'package', ['package_id'], ['id'])
        batch_op.create_foreign_key('fk_report_customer_id', 'customer', ['customer_id'], ['id'])
        batch_op.create_foreign_key('fk_report_vehicle_id', 'vehicle', ['vehicle_id'], ['id'])
        batch_op.create_foreign_key('fk_report_created_by', 'staff', ['created_by'], ['id'])

    # Remove the default values if not needed after adding the columns
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.alter_column('vehicle_id', server_default=None)
        batch_op.alter_column('customer_id', server_default=None)
        batch_op.alter_column('package_id', server_default=None)
        batch_op.alter_column('created_by', server_default=None)
        batch_op.alter_column('registration_document_seen', server_default=None)


def downgrade():
    # Use batch mode for SQLite-compatible downgrade
    with op.batch_alter_table('report', schema=None) as batch_op:
        # Drop constraints by their names
        batch_op.drop_constraint('fk_report_package_id', type_='foreignkey')
        batch_op.drop_constraint('fk_report_customer_id', type_='foreignkey')
        batch_op.drop_constraint('fk_report_vehicle_id', type_='foreignkey')
        batch_op.drop_constraint('fk_report_created_by', type_='foreignkey')

        # Drop columns (if needed)
        batch_op.drop_column('registration_document_seen')
        batch_op.drop_column('created_by')
        batch_op.drop_column('created_at')
        batch_op.drop_column('operation')
        batch_op.drop_column('package_id')
        batch_op.drop_column('customer_id')
        batch_op.drop_column('vehicle_id')

