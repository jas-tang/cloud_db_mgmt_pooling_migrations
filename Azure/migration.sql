CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 342856222981

INSERT INTO alembic_version (version_num) VALUES ('342856222981');

-- Running upgrade 342856222981 -> 15c8a7f71120

ALTER TABLE patients ADD COLUMN azure_is_active VARCHAR(50) NOT NULL;

UPDATE alembic_version SET version_num='15c8a7f71120' WHERE alembic_version.version_num = '342856222981';

