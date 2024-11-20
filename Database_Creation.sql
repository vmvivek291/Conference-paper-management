-- Create Database : 
CREATE DATABASE CPMS;
USE CPMS;

-- Create tables : 

-- Authors Table
CREATE TABLE Authors (
    Author_ID VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Age INT,
    Email VARCHAR(50) UNIQUE,
    Bio TEXT,
    Password VARCHAR(50) NOT NULL
);

-- Research Interest Table
CREATE TABLE Research_Interest (
    Author_ID VARCHAR(50) PRIMARY KEY,
    Research_interest VARCHAR(50),
    FOREIGN KEY (Author_ID) REFERENCES Authors(Author_ID)
);

-- Conference Table
CREATE TABLE Conference (
    Conference_ID VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(50),
    Location VARCHAR(50),
    Date DATE,
    Organizer VARCHAR(50)
);

-- Proceedings Table
CREATE TABLE Proceedings (
    Conference_ID VARCHAR(50),
    ISSN VARCHAR(50) UNIQUE,
    Volume INT,
    Number_of_pages INT DEFAULT 0,
    PRIMARY KEY (Conference_ID, ISSN),
    FOREIGN KEY (Conference_ID) REFERENCES Conference(Conference_ID)
);

-- Reviewer Table
CREATE TABLE Reviewer (
    Reviewer_ID VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Password VARCHAR(50) NOT NULL,
    Email VARCHAR(50) UNIQUE,
    Conference_ID VARCHAR(50),
    FOREIGN KEY (Conference_ID) REFERENCES Conference(Conference_ID)
);

-- Papers Table
CREATE TABLE Papers (
    Paper_ID VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(50) UNIQUE,
    Abstract TEXT,
    Category VARCHAR(50),
    Status VARCHAR(50),
    Version INT,
    Reviewer_ID VARCHAR(50),
    Feedback TEXT,
    Conference_ID VARCHAR(50),
    Manuscript BLOB,
    FOREIGN KEY (Reviewer_ID) REFERENCES Reviewer(Reviewer_ID),
    FOREIGN KEY (Conference_ID) REFERENCES Conference(Conference_ID)
);

-- Paper_Uploads Table
CREATE TABLE Paper_Uploads (
    Author_ID VARCHAR(50),
    Paper_ID VARCHAR(50),
    Submission_date DATE,
    PRIMARY KEY (Author_ID, Paper_ID),
    FOREIGN KEY (Author_ID) REFERENCES Authors(Author_ID),
    FOREIGN KEY (Paper_ID) REFERENCES Papers(Paper_ID)
);

-- Registration Table
CREATE TABLE Registration (
    RegistrationType ENUM('Author', 'Reviewer') NOT NULL,
    Name VARCHAR(50) NOT NULL,
    Password VARCHAR(50) NOT NULL,
    Author_ID VARCHAR(50) DEFAULT NULL,
    Reviewer_ID VARCHAR(50) DEFAULT NULL,
    UNIQUE (Author_ID),
    UNIQUE (Reviewer_ID)
);


-- Insert values into tables : 

-- Insert values into Authors table
-- INSERT INTO Authors (Author_ID, Name, Age, Email, Bio, Password) VALUES
-- ('A001', 'Alice Johnson', 35, 'alice.johnson@example.com', 'Expert in AI and ML', 'password123'),
-- ('A002', 'Bob Smith', 40, 'bob.smith@example.com', 'Data Scientist', 'password456'),
-- ('A003', 'Carol White', 28, 'carol.white@example.com', 'Researcher in NLP', 'password789'),
-- ('A004', 'David Brown', 50, 'david.brown@example.com', 'Professor in Quantum Computing', 'password321'),
-- ('A005', 'Eve Davis', 32, 'eve.davis@example.com', 'Cloud Computing Specialist', 'password654'),
-- ('A006', 'Frank Martin', 45, 'frank.martin@example.com', 'Expert in Computer Vision', 'password987'),
-- ('A007', 'Grace Lee', 30, 'grace.lee@example.com', 'Cryptography Enthusiast', 'password147'),
-- ('A008', 'Henry Wilson', 27, 'henry.wilson@example.com', 'Cybersecurity Analyst', 'password258'),
-- ('A009', 'Ivy Scott', 34, 'ivy.scott@example.com', 'Data Engineering Expert', 'password369');

-- Insert values into Research_Interest table
-- INSERT INTO Research_Interest (Author_ID, Research_interest) VALUES
-- ('A001', 'Machine Learning'),
-- ('A002', 'Data Science'),
-- ('A003', 'Natural Language Processing'),
-- ('A004', 'Quantum Computing'),
-- ('A005', 'Cloud Computing'),
-- ('A006', 'Computer Vision'),
-- ('A007', 'Cryptography'),
-- ('A008', 'Cybersecurity'),
-- ('A009', 'Data Engineering');

-- Insert values into Conference table
-- INSERT INTO Conference (Conference_ID, Name, Location, Date, Organizer) VALUES
-- ('C001', 'International Conference on AI', 'New York', '2024-06-15', 'ICAI'),
-- ('C002', 'Quantum Computing Symposium', 'San Francisco', '2024-09-20', 'QCS'),
-- ('C003', 'Data Science Summit', 'Chicago', '2024-11-05', 'DSS');

-- Insert values into Proceedings table
-- INSERT INTO Proceedings (Conference_ID, ISSN, Volume, Number_of_pages) VALUES
-- ('C001', 'ISSN001', 1, 120),
-- ('C002', 'ISSN002', 1, 100),
-- ('C003', 'ISSN003', 1, 200);

-- Insert values into Reviewer table
-- INSERT INTO Reviewer (Reviewer_ID, Name, Password, Email, Conference_ID) VALUES
-- ('R001', 'Michael Brown', 'revpass123', 'michael.brown@example.com', 'C001'),
-- ('R002', 'Nancy Green', 'revpass456', 'nancy.green@example.com', 'C002'),
-- ('R003', 'Oliver King', 'revpass789', 'oliver.king@example.com', 'C003');

-- Insert values into Papers table
-- INSERT INTO Papers (Paper_ID, Title, Abstract, Category, Status, Version, Reviewer_ID, Feedback, Conference_ID) VALUES
-- ('P001', 'AI in Healthcare', 'Research on AI applications in healthcare', 'AI', 'Accepted', 1, 'R001', 'Promising research', 'C001'),
-- ('P002', 'Quantum Cryptography', 'Advanced methods in quantum cryptography', 'Quantum Computing', 'Under Review', 1, 'R002', NULL, 'C002'),
-- ('P003', 'Data Pipelines', 'Efficient data pipelines for big data', 'Data Engineering', 'Accepted', 2, 'R003', 'Well-documented methods', 'C003'),
-- ('P004', 'AI Ethics', 'Ethical considerations in AI', 'AI', 'Under Review', 1, 'R001', NULL, 'C001'),
-- ('P005', 'Cloud Security', 'Enhancing security in cloud environments', 'Cloud Computing', 'Accepted', 1, 'R001', 'Good structure', 'C001'),
-- ('P006', 'Deep Learning for NLP', 'Applications of deep learning in NLP', 'NLP', 'Accepted', 1, 'R002', 'Interesting approach', 'C002'),
-- ('P007', 'Data Privacy', 'Challenges in data privacy', 'Cybersecurity', 'Accepted', 1, 'R003', 'Important topic', 'C003'),
-- ('P008', 'ML in Finance', 'Machine learning applications in finance', 'AI', 'Accepted', 2, 'R001', 'Clear analysis', 'C001'),
-- ('P009', 'Edge Computing', 'Optimizations in edge computing', 'Cloud Computing', 'Under Review', 1, 'R002', NULL, 'C002');

-- Insert values into Paper_Uploads table
-- INSERT INTO Paper_Uploads (Author_ID, Paper_ID, Submission_date) VALUES
-- ('A001', 'P001', '2024-03-01'),
-- ('A002', 'P002', '2024-03-15'),
-- ('A003', 'P003', '2024-04-10'),
-- ('A001', 'P004', '2024-04-20'),
-- ('A005', 'P005', '2024-04-25'),
-- ('A004', 'P006', '2024-05-01'),
-- ('A007', 'P007', '2024-05-10'),
-- ('A008', 'P008', '2024-05-20'),
-- ('A009', 'P009', '2024-05-30'),
-- ('A002', 'P005', '2024-04-25');

-- Explanation of the Criteria Fulfillment
-- 9-10 values in each table: Each table has been populated with around 9–10 entries.
-- Same author with 2 papers: Author A001 has both P001 and P004.
-- One paper with multiple authors: Paper P005 has both A005 and A002.
-- Reviewer reviewing multiple papers: Reviewer R001 is assigned to P001, P004, P005, and P008.
-- Three conferences: There are three conferences (C001, C002, C003).
-- Conference with multiple proceedings: Conference C001 has two proceedings (ISSN001, Volumes 1 and 2).
-- Proceeding with multiple papers: Papers P001, P004, P005, and P008 are all in Conference_ID = C001 (linked to ISSN001).


-- Insert Author data into Registration table
-- INSERT INTO Registration (RegistrationType, Name, Password, Author_ID)
-- SELECT 'Author', Name, Password, Author_ID
-- FROM Authors;

-- Insert Reviewer data into Registration table
-- INSERT INTO Registration (RegistrationType, Name, Password, Reviewer_ID)
-- SELECT 'Reviewer', Name, Password, Reviewer_ID
-- FROM Reviewer;


-- Trigger to generate a new Paper_ID
-- DELIMITER //
-- CREATE TRIGGER before_insert_papers
-- BEFORE INSERT ON papers
-- FOR EACH ROW
-- BEGIN
--     DECLARE new_id VARCHAR(50);
--     CALL GenerateNextID('P', new_id, 'papers', 'Paper_ID');
--     SET NEW.Paper_ID = new_id;
-- END //
-- DELIMITER ;

-- Trigger to generate a new Conference_ID
-- DELIMITER //
-- CREATE TRIGGER before_insert_conference
-- BEFORE INSERT ON conference
-- FOR EACH ROW
-- BEGIN
--     DECLARE new_id VARCHAR(50);
--     CALL GenerateNextID('C', new_id, 'conference', 'Conference_ID');
--     SET NEW.Conference_ID = new_id;
-- END //
-- DELIMITER ;


-- Trigger to generate a new Reviewer_ID
-- DELIMITER //
-- CREATE TRIGGER before_insert_reviewer
-- BEFORE INSERT ON Reviewer
-- FOR EACH ROW
-- BEGIN
--     DECLARE new_id VARCHAR(50);
--     CALL GenerateNextID('R', new_id, 'Reviewer', 'Reviewer_ID');
--     SET NEW.Reviewer_ID = new_id;
-- END //
-- DELIMITER ;


-- Trigger to generate a new Author_ID
-- DELIMITER //
-- CREATE TRIGGER before_insert_author
-- BEFORE INSERT ON Authors
-- FOR EACH ROW
-- BEGIN
--     DECLARE new_id VARCHAR(50);
--     CALL GenerateNextID('A', new_id, 'Authors', 'Author_ID');
--     SET NEW.Author_ID = new_id;
-- END //
-- DELIMITER ;


-- Procedure to generate the next ID for either paper, conference, author or reviewer
-- DELIMITER //
-- CREATE PROCEDURE GenerateNextID(IN prefix CHAR(1), OUT new_id VARCHAR(50), IN table_name VARCHAR(50), IN column_name VARCHAR(50))
-- BEGIN
--     DECLARE max_id INT;
--     DECLARE query VARCHAR(255);
--     
--     -- Hard-code the table and column for simplicity
--     IF table_name = 'Papers' AND column_name = 'Paper_ID' THEN
--         -- Retrieve the maximum Paper_ID (assuming it's in the format 'P001', 'P002', etc.)
--         SELECT COALESCE(MAX(CAST(SUBSTRING(Paper_ID, 2) AS UNSIGNED)), 0) INTO max_id
--         FROM Papers;
--     ELSEIF table_name = 'Reviewer_paper' AND column_name = 'Reviewer_ID' THEN
--         -- Retrieve the maximum Reviewer_ID
--         SELECT COALESCE(MAX(CAST(SUBSTRING(Reviewer_ID, 2) AS UNSIGNED)), 0) INTO max_id
--         FROM Reviewer_paper;
--     ELSEIF table_name = 'Authors' AND column_name = 'Author_ID' THEN
--         -- Retrieve the maximum Author_ID
--         SELECT COALESCE(MAX(CAST(SUBSTRING(Author_ID, 2) AS UNSIGNED)), 0) INTO max_id
--         FROM Authors;
--     ELSE
--         -- Add more table/column combinations as needed
--         SET max_id = 0;
--     END IF;

--     -- Increment the max ID and create the new ID with the specified prefix
--     SET new_id = CONCAT(prefix, LPAD(max_id + 1, 3, '0'));
-- END //
-- DELIMITER ;

-- Query to fetch all papers that have status = "Accepted"
-- SELECT p.Paper_ID, p.Title, c.Name
--             FROM Papers p
--             JOIN Paper_Uploads pu ON p.Paper_ID = pu.Paper_ID
--             JOIN Conference c ON p.Conference_ID = c.Conference_ID
--             WHERE pu.Author_ID = %s AND p.Status = 'Accepted'


-- Query to show all papers submitted in descending order of date
-- SELECT p.Paper_ID, p.Title, pu.Submission_date
--             FROM Papers p
--             JOIN Paper_Uploads pu ON p.Paper_ID = pu.Paper_ID
--             WHERE pu.Author_ID = %s
--             ORDER BY pu.Submission_date DESC


-- Query to fetch paper based on the search for paper ID
-- SELECT 
--                 p.Paper_ID,
--                 p.Title,
--                 p.Status,
--                 pu.Submission_date,
--                 c.Name as Conference_Name
--             FROM Papers p
--             JOIN Paper_Uploads pu ON p.Paper_ID = pu.Paper_ID
--             JOIN Conference c ON p.Conference_ID = c.Conference_ID
--             WHERE p.Paper_ID = %s AND pu.Author_ID = %s


-- Procedure to Insert paper into Paper_Uploads
-- DELIMITER //
-- CREATE PROCEDURE InsertIntoPaperUploads(IN author_id varchar(50), IN paper_id varchar(50))
-- BEGIN
--     DECLARE today_date INT;
--     SELECT curdate() into today_date;
--     INSERT INTO Paper_Uploads (Author_ID, Paper_ID, Submission_date) VALUES (author_id,paper_id,today_date);
-- END //
-- DELIMITER ;


-- To randomly assign reviewer for the given paper uploaded.
-- UPDATE Papers AS p
-- SET Reviewer_ID = (
--     SELECT Reviewer_ID
--     FROM Reviewer AS r
--     WHERE r.Conference_ID = p.Conference_ID
--     ORDER BY RAND()
--     LIMIT 1
-- )
-- WHERE p.Conference_ID IS NOT NULL;

-- View to create a table with relevant information to perform an effective search operation
CREATE VIEW Author_Conference_Papers AS
SELECT 
    au.Author_ID,
    au.Name AS Author_Name,
    c.Conference_ID,
    c.Name AS Conference_Name,
    p.Paper_ID,
    p.Title AS Paper_Title,
    p.Abstract AS Paper_Abstract,
    p.Category AS Paper_Category,
    p.Status AS Paper_Status,
    p.Manuscript
FROM 
    Authors au
JOIN 
    Paper_Uploads pu ON au.Author_ID = pu.Author_ID
JOIN 
    Papers p ON pu.Paper_ID = p.Paper_ID
JOIN 
    Conference c ON p.Conference_ID = c.Conference_ID
WHERE 
    p.Status = 'Accepted';

    
select * from Author_Conference_Papers;
DROP VIEW IF EXISTS Author_Conference_Papers;

-- Query to filter based on Author_Name
SELECT 
    Author_Name, 
    Conference_Name, 
    Paper_Title, 
    Paper_Category, 
    Manuscript 
FROM 
    Author_Conference_Papers 
WHERE 
    Author_Name = 'given_author_name';

-- Query to filter based on Paper_Title
SELECT 
    Author_Name, 
    Conference_Name, 
    Paper_Title, 
    Paper_Category, 
    Manuscript 
FROM 
    Author_Conference_Papers 
WHERE 
    Paper_Title = 'given_paper_title';

-- Query to filter based on Paper_Category
SELECT 
    Author_Name, 
    Conference_Name, 
    Paper_Title, 
    Paper_Category, 
    Manuscript 
FROM 
    Author_Conference_Papers 
WHERE 
    Paper_Category = 'given_paper_category';


CREATE ROLE Webuser;
CREATE ROLE Author;
CREATE ROLE Reviewer;

GRANT SELECT ON CPMS.* TO Webuser;
GRANT SELECT, INSERT ON CPMS.* TO Author;
GRANT SELECT, INSERT, UPDATE ON CPMS.* TO Reviewer;

-- Create a user for Webuser role
CREATE USER 'vedant'@'localhost' IDENTIFIED BY 'vedant';
GRANT Webuser TO 'vedant'@'localhost';

-- Create a user for Author role
CREATE USER 'Alice'@'localhost' IDENTIFIED BY 'password123';
GRANT Author TO 'Alice'@'localhost';

-- Create a user for Reviewer role
CREATE USER 'Michael'@'localhost' IDENTIFIED BY 'revpass123';
GRANT Reviewer TO 'Michael'@'localhost';

-- Make Webuser role active by default for user 'vedant'
ALTER USER 'vedant'@'localhost' DEFAULT ROLE Webuser;

-- Make Author role active by default for user 'Alice'
ALTER USER 'Alice'@'localhost' DEFAULT ROLE Author;

-- Make Reviewer role active by default for user 'Michael'
ALTER USER 'Michael'@'localhost' DEFAULT ROLE Reviewer;


SELECT 
    GRANTEE, 
    PRIVILEGE_TYPE, 
    TABLE_SCHEMA 
FROM 
    information_schema.schema_privileges
WHERE 
    TABLE_SCHEMA = 'CPMS';


-- As webuser
-- SELECT * FROM CPMS.Authors;       -- Should work
-- INSERT INTO CPMS.Authors VALUES (...); -- Should be denied

-- As author_user
-- SELECT * FROM CPMS.Papers;       -- Should work
-- INSERT INTO CPMS.Papers VALUES (...); -- Should work
-- UPDATE CPMS.Papers SET Title = 'New Title' WHERE Paper_ID = 'P001'; -- Should be denied

-- As reviewer_user
-- SELECT * FROM CPMS.Reviewer;       -- Should work
-- INSERT INTO CPMS.Reviewer VALUES (...); -- Should work
-- UPDATE CPMS.Papers SET Status = 'Accepted' WHERE Paper_ID = 'P001'; -- Should work


-- To show all triggers listed in the paper
-- SELECT 
--     TRIGGER_NAME,
--     EVENT_MANIPULATION AS EVENT,
--     EVENT_OBJECT_TABLE AS TABLE_NAME,
--     ACTION_STATEMENT AS DEFINITION,
--     ACTION_TIMING AS TIMING,
--     CREATED
-- FROM 
--     information_schema.TRIGGERS
-- WHERE 
--     TRIGGER_SCHEMA = 'CPMS';
