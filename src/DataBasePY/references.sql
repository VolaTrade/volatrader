
-- Create paper trader table query --
CREATE TABLE papertrader_results (
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
    indicators jsonb NOT NULL DEFAULT '[]'::jsonb,
    transactions jsonb NOT NULL DEFAULT '[]'::jsonb,
    users_tracking jsonb NOT NULL DEFAULT '[]'::jsonb, 
);

-- Create support/resistance table query -- 

CREATE TABLE support_resistance (
	ts timestamp,
    pair pair,
    candle candle,
    support numeric,
    resistance numeric,
    UNIQUE (pair, candle)
);


-- Create statistic table to hold volume data -- 
CREATE TABLE STATISTIC_TABLE(
	pair pair,
	candle candle,
	mean_volume numeric,
	volume_sd numeric
);

-- Create backtest result table to hold backtest data --
CREATE TABLE BACKTEST_RESULTS(
    time_stamp character varying,
    strategy strategy,
    version numeric,
    pair pair,
    candle candle,
    takeprofit NUMERIC(5,3),
    stoploss NUMERIC(5,3),
    indicator_values jsonb, 
    timeframe character varying,
    score character varying,
    beta_score character varying
);

-- CREATE strategies table to hold strat information -- 

CREATE TABLE STRATEGIES(
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    strategy strategy, 
    version_number numeric, 
    source character varying
);

