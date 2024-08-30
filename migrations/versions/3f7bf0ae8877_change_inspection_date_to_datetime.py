"""Change inspection_date to DateTime

Revision ID: 3f7bf0ae8877
Revises: 
Create Date: 2024-08-30 00:56:34.133650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f7bf0ae8877'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table with the desired column types
    op.create_table('report_new',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('inspection_date', sa.DateTime(), nullable=False),
                    sa.Column('vehicle_id', sa.Integer(), nullable=False, default=0),  # Provide a default value
                    # Add other columns as needed
                    )

    # Copy data from the old table to the new table
    op.execute('INSERT INTO report_new (id, inspection_date, vehicle_id) SELECT id, inspection_date, 0 FROM report')

    # Drop the old table
    op.drop_table('report')

    # Rename the new table to the old table's name
    op.rename_table('report_new', 'report')


def downgrade():
    # Create the original table structure
    op.create_table('report_old',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('inspection_date', sa.DATE(), nullable=False),
                    # Add other columns as needed
                    )

    # Copy data back from the new table to the old table
    op.execute('INSERT INTO report_old (id, inspection_date) SELECT id, inspection_date FROM report')

    # Drop the new table
    op.drop_table('report')

    # Rename the old table back to the original name
    op.rename_table('report_old', 'report')
