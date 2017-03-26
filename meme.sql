
CREATE TABLE Users
(
uid INTEGER NOT NULL PRIMARY KEY,
name VARCHAR(256) NOT NULL,
password VARCHAR(256) NOT NULL,
avatar VARCHAR(256) 
-- CHECK(LEN(password)>10)
);

CREATE TABLE Meme
(
memeID INTEGER NOT NULL PRIMARY KEY,
caption VARCHAR(256) NOT NULL,
filepath VARCHAR(256) NOT NULL,
imagename VARCHAR(256) NOT NULL
);

CREATE TABLE TAG
(
name VARCHAR(256) NOT NULL PRIMARY KEY
);

CREATE TABLE IsFriend
(
uid INTEGER NOT NULL REFERENCES Users(uid),
friend INTEGER NOT NULL REFERENCES Users(uid),
PRIMARY KEY(uid,friend)
);

CREATE TABLE PotentialPartner
(
uid INTEGER NOT NULL REFERENCES Users(uid),
partner INTEGER NOT NULL REFERENCES Users(uid),
PRIMARY KEY (uid, partner)
);

CREATE TABLE Opinion
(
uid INTEGER NOT NULL REFERENCES Users(uid),
memeID INTEGER NOT NULL REFERENCES Meme(memeID),
preference INTEGER NOT NULL 
-- #0=neutral, 1=likes, -1=dislike
);

CREATE TABLE HasTag
(
memeID INTEGER NOT NULL REFERENCES Meme(memeID),
tagName VARCHAR(256) NOT NULL REFERENCES Tag(name),
PRIMARY KEY(memeID,tagName)
);

-- check if the memes exist in the database or not 
CREATE FUNCTION Add_To_Meme_Table() RETURNS TRIGGER AS $$
BEGIN 
	IF EXISTS (Select * from Meme WHERE NEW.caption = Meme.caption) THEN
	RAISE EXCEPTION '% : Duplicate Meme', NEW.Caption;
	END IF; 
	RETURN NEW; 
END;
$$ LANGUAGE plpgsql;

-- check if the tag exist in the database or not
CREATE TRIGGER Add_To_Meme_Table
	BEFORE INSERT ON Meme
	FOR EACH ROW
	EXECUTE PROCEDURE Add_To_Meme_Table();
    
    
CREATE FUNCTION Add_To_Tag_Table() RETURNS TRIGGER AS $$
BEGIN 
	IF NOT EXISTS (Select * from Tag WHERE NEW.tagName = Tag.name) THEN
    INSERT INTO TAG VALUES(NEW.tagName);
	END IF; 
	RETURN NEW; 
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER Add_To_Tag_Table
	BEFORE INSERT ON HasTag
	FOR EACH ROW
	EXECUTE PROCEDURE Add_To_Tag_Table();

#hand-populated small dataset

INSERT INTO Users VALUES(1,'JOYCE DA BOMB.COM','JerryDatingApp',NULL);
INSERT INTO Users VALUES(2,'Jerry','894836',NULL);
INSERT INTO Users VALUES(3,'Mom','7485926',NULL);
INSERT INTO Users VALUES(4,'Dad','986246',NULL);
INSERT INTO Users VALUES(5,'Jessica','346467',NULL);
INSERT INTO Users VALUES(6, 'Molly','iluvchocolate',NULL);
INSERT INTO Users VALUES(7, 'Fangge','chasegarcia',NULL);
INSERT INTO Users VALUES(8, 'Naijiao','im-fun-n-flirty',NULL);
INSERT INTO Users VALUES(9, 'Joyce Choi','gurlzwhocod3',NULL);
INSERT INTO Users VALUES(10, 'NANA','i_rock',NULL);

INSERT INTO Meme VALUES(1,'3_days_later_2','../memes/faces/3_days_later_2.jpg','3_days_later_2' );
INSERT INTO Meme VALUES(2,'3_hours_later','../static/media/faces/3_hours_later.jpg','3_hours_later' );
INSERT INTO Meme VALUES(3,'baby_troll','../memes/faces/baby_troll.jpg','baby_troll');
INSERT INTO Meme VALUES(4,'beng','../memes/faces/beng.jpg','beng');
INSERT INTO Meme VALUES(5,'aint_that_some_shit','../memes/faces/aint_that_some_shit.jpg','aint_that_some_shit');
INSERT INTO Meme VALUES(6,'aww_yeah','../memes/faces/aww_yeah.jpg','aww_yeah');
INSERT INTO Meme VALUES(7,'dat_ass','../memes/faces/dat_ass.jpg','dat_ass');
INSERT INTO Meme VALUES(8,'damn','../memes/faces/damn.jpg','damn');
INSERT INTO Meme VALUES(9,'fap_scream','../memes/faces/fap_scream.jpg','fap_scream'); #nastyassmofo
INSERT INTO Meme VALUES(10,'first_world_problems','../memes/faces/first_world_problems.jpg','first_world_problems');
INSERT INTO Meme VALUES(11,'fuck_that_yao_ming','../memes/faces/fuck_that_yao_ming.jpg','fuck_that_yao_ming');
INSERT INTO Meme VALUES(12,'high_expectations_asian_father','../memes/faces/high_expectations_asian_father.jpg','high_expectations_asian_father');

INSERT INTO Tag VALUES('time');
INSERT INTO Tag VALUES('spongebob');
INSERT INTO Tag VALUES('animal');
INSERT INTO Tag VALUES('face');
INSERT INTO Tag VALUES('cat');
INSERT INTO Tag VALUES('dog');
INSERT INTO Tag VALUES('guy');
INSERT INTO Tag VALUES('girl');
INSERT INTO Tag VALUES('funny');
INSERT INTO Tag VALUES('gross');
INSERT INTO Tag VALUES('scary');

INSERT INTO isFriend VALUES(1, 3);
INSERT INTO isFriend VALUES(2, 4);

INSERT INTO PotentialPartner VALUES(1, 5);
INSERT INTO PotentialPartner VALUES(2, 5);

INSERT INTO Opinion VALUES(2, 1, 1);
INSERT INTO Opinion VALUES(2, 2, 3);
INSERT INTO Opinion VALUES(2, 3, 3);

INSERT INTO HasTag VALUES(2, 'time');
INSERT INTO HasTag VALUES(2, 'spongebob');
INSERT INTO HasTag VALUES('animal');
INSERT INTO HasTag VALUES('face');
INSERT INTO HasTag VALUES('cat');
INSERT INTO HasTag VALUES('dog');
INSERT INTO HasTag VALUES('guy');
INSERT INTO HasTag VALUES('girl');
INSERT INTO HasTag VALUES('funny');
INSERT INTO HasTag VALUES('gross');
INSERT INTO HasTag VALUES('scary');

Select * from Users; 
Select * from Meme; 
Select * from Tag;
Select * from IsFriend;
Select * from PotentialPartner; 
Select * from Opinion; 
Select * from HasTag; 




