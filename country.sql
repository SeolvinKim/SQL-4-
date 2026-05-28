DROP SCHEMA IF EXISTS edu_country CASCADE;
CREATE SCHEMA edu_country;

-- 1. countries (국가 테이블)
CREATE TABLE edu_country.countries (
    country_code CHAR(2) PRIMARY KEY, -- ISO 3166-1 alpha-2 기준 (예: KR)
    country_name VARCHAR(100) NOT NULL UNIQUE,
    continent VARCHAR(50) NOT NULL,
    population BIGINT CHECK (population >= 0) -- 인구수는 0 이상이어야 함
);

-- 2. cities (도시 테이블)
CREATE TABLE edu_country.cities (
    city_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    city_name VARCHAR(100) NOT NULL,
    country_code CHAR(2) NOT NULL REFERENCES edu_country.countries(country_code) ON DELETE CASCADE,
    is_capital BOOLEAN NOT NULL DEFAULT FALSE
);

-- 3. languages (국가별 언어 테이블)
CREATE TABLE edu_country.languages (
    language_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    country_code CHAR(2) NOT NULL REFERENCES edu_country.countries(country_code) ON DELETE CASCADE,
    language_name VARCHAR(50) NOT NULL,
    is_official BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (country_code, language_name) -- 한 국가 내에서 동일한 언어 중복 등록 방지
);

-- 4. landmarks (랜드마크 테이블)
CREATE TABLE edu_country.landmarks (
    landmark_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    landmark_name VARCHAR(150) NOT NULL,
    country_code CHAR(2) NOT NULL REFERENCES edu_country.countries(country_code) ON DELETE CASCADE,
    city_id UUID REFERENCES edu_country.cities(city_id) ON DELETE SET NULL, -- 도시가 삭제되어도 랜드마크 기록은 유지하되 참조만 Null 처리
    established_year INTEGER CHECK (established_year <= EXTRACT(YEAR FROM CURRENT_DATE)) -- 미래 연도 입력 방지
);

-- 5. currencies (통화 테이블)
CREATE TABLE edu_country.currencies (
    currency_code CHAR(3) NOT NULL, -- ISO 4217 기준 (예: KRW)
    country_code CHAR(2) NOT NULL REFERENCES edu_country.countries(country_code) ON DELETE CASCADE,
    currency_name VARCHAR(50) NOT NULL,
    exchange_rate NUMERIC(15, 6) CHECK (exchange_rate > 0), -- 환율은 0보다 커야 함
    PRIMARY KEY (currency_code, country_code) -- 여러 국가가 같은 통화(예: EUR)를 사용할 수 있으므로 복합키 사용
);

-- 1. countries (국가 데이터)
INSERT INTO edu_country.countries (country_code, country_name, continent, population) VALUES
('KR', 'South Korea', 'Asia', 51780000),
('US', 'United States', 'North America', 331900000),
('FR', 'France', 'Europe', 67900000),
('JP', 'Japan', 'Asia', 125800000),
('CA', 'Canada', 'North America', 38900000),
('CN', 'China', 'Asia', 1412000000),
('SG', 'Singapore', 'Asia', 5900000),
('PH', 'Philippines', 'Asia', 113900000),
('DE', 'Germany', 'Europe', 83200000),
('GB', 'United Kingdom', 'Europe', 67300000);

-- 2. cities (도시 데이터)
INSERT INTO edu_country.cities (city_name, country_code, is_capital) VALUES
('Seoul', 'KR', TRUE),
('New York', 'US', FALSE),
('Paris', 'FR', TRUE);

-- 3. languages (언어 데이터)
INSERT INTO edu_country.languages (country_code, language_name, is_official) VALUES
('KR', 'Korean', TRUE),
('US', 'English', TRUE),
('FR', 'French', TRUE);

-- 4. landmarks (랜드마크 데이터)
INSERT INTO edu_country.landmarks (landmark_name, country_code, city_id, established_year) VALUES
('Gyeongbokgung Palace', 'KR', (SELECT city_id FROM edu_country.cities WHERE city_name = 'Seoul'), 1395),
('Statue of Liberty', 'US', (SELECT city_id FROM edu_country.cities WHERE city_name = 'New York'), 1886),
('Eiffel Tower', 'FR', (SELECT city_id FROM edu_country.cities WHERE city_name = 'Paris'), 1889);

-- 5. currencies (통화 데이터)
INSERT INTO edu_country.currencies (currency_code, country_code, currency_name, exchange_rate) VALUES
('KRW', 'KR', 'South Korean Won', 1350.50),
('USD', 'US', 'US Dollar', 1.00),
('EUR', 'FR', 'Euro', 0.92),
('JPY', 'JP', 'Japanese Yen', 9.15),
('CAD', 'CA', 'Canadian Dollar', 1015.30),
('CNY', 'CN', 'Chinese Yuan', 188.45),
('SGD', 'SG', 'Singapore Dollar', 1023.80),
('PHP', 'PH', 'Philippine Peso', 24.10),
('EUR', 'DE', 'Euro', 1485.70),
('GBP', 'GB', 'British Pound', 1732.40);
-- ------------------------------------------------------------
-- 1. 국가 수, 평균 인구, 최고 인구, 최저 인구를 한 번에 조회하기
-- ------------------------------------------------------------
SELECT
    COUNT(country_code) AS count_c, 
    ROUND(AVG(population),2) AS avg_p,
    MAX(population) AS max_p,
    MIN(population) AS min_p
FROM edu_country.countries;
-- ------------------------------------------------------------
-- 2. 언어 종류 목록 만들기
-- ------------------------------------------------------------
SELECT
    DISTINCT language_name
FROM edu_country.languages;
-- ------------------------------------------------------------
-- 3. 전체 국가에서 영어를 사용하는 나라의 비율
-- ------------------------------------------------------------
SELECT 
    COUNT(DISTINCT CASE 
        WHEN language_name = 'English' THEN country_code 
    END) * 100.0 
    / COUNT(DISTINCT country_code) AS english_usage_ratio
FROM edu_country.languages;
-- ------------------------------------------------------------
-- 4. 전세계 인구 중 한국어를 사용하는 나라 비율
-- ------------------------------------------------------------
SELECT 
    ROUND(
        SUM(
            CASE 
                WHEN l.language_name = 'Korean' 
                THEN c.population
                ELSE 0
            END
        ) * 100.0
        / SUM(c.population),
        2
    ) AS korean_speaking_population_ratio
FROM edu_country.countries c
JOIN edu_country.languages l
    ON c.country_code = l.country_code;
-- ------------------------------------------------------------
-- 5. 전세계 인구 중 currency_code를 EUR를 사용하는 사람의 수
-- ------------------------------------------------------------
SELECT 
    cu.currency_code,
    SUM(c.population) AS eur_using_population
FROM edu_country.currencies cu
JOIN edu_country.countries c
    ON cu.country_code = c.country_code
WHERE cu.currency_code = 'EUR'
GROUP BY cu.currency_code;
