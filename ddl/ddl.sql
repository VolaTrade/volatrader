
-- Create paper trader table query --
CREATE TABLE papertrades (
    session_id uuid PRIMARY KEY,
    running_on character varying,
    session_start_time timestamp,
    session_end_time timestamp,
    strategy character varying,
    pair pair,
    candle candle,
    stoploss NUMERIC(5,3),
    takeprofit NUMERIC(5,3),
    active boolean,
    total_pnl NUMERIC(8, 4),
    principle NUMERIC(14, 2),
    transactions jsonb NOT NULL DEFAULT '[]'::jsonb,
);


-- CREATE strategies table to hold strat information -- 

CREATE TABLE STRATEGIES(
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    strategy strategy, 
    version_number numeric, 
    source character varying
);

