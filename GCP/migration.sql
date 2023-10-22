CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 4ddf04bb5782

INSERT INTO alembic_version (version_num) VALUES ('4ddf04bb5782');

-- Running upgrade 4ddf04bb5782 -> e31e6d5e4817

ALTER TABLE patients ADD COLUMN is_active VARCHAR(50) NOT NULL;

UPDATE alembic_version SET version_num='e31e6d5e4817' WHERE alembic_version.version_num = '4ddf04bb5782';

