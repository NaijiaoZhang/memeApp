
CREATE TABLE Users
(
uid INTEGER NOT NULL PRIMARY KEY,
name VARCHAR(256) NOT NULL,
password VARCHAR(25) NOT NULL,
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


INSERT INTO Users VALUES(1,'JOYCE DA BOMB.COM','JerryDatingApp',NULL);
INSERT INTO Users VALUES(2,'Jerry','894836',NULL);
INSERT INTO Users VALUES(3,'Mom','7485926',NULL);
INSERT INTO Users VALUES(4,'Dad','986246',NULL);
INSERT INTO Users VALUES(5,'Jessica','346467',NULL);

INSERT INTO Meme VALUES(1,'Kreygasm!!~~~','./here','Twitch Face' );
INSERT INTO Meme VALUES(2,'Kreygasm!!~~~','./here','Funny' );
INSERT INTO Meme VALUES(2,'LuL','./here','Funny' );
INSERT INTO Meme VALUES(3,'Life','./here','Hamster');
INSERT INTO Meme VALUES(4,'FML','./here','Drowning');

INSERT INTO TAG VALUES('frog');
INSERT INTO TAG VALUES('box');

INSERT INTO isFriend VALUES(1, 3);
INSERT INTO isFriend VALUES(2, 4);

INSERT INTO PotentialPartner VALUES(1, 5);
INSERT INTO PotentialPartner VALUES(2, 5);

INSERT INTO Opinion VALUES(2, 1, 1);
INSERT INTO Opinion VALUES(2, 2, 3);
INSERT INTO Opinion VALUES(2, 3, 3);

INSERT INTO HasTag VALUES(2, 'frog');
INSERT INTO HasTag VALUES(2, 'box');

Select * from users; 
Select * from Meme; 
Select * from tag;
Select * from isFriend;
Select * from potentialpartner; 
Select * from opinion; 
Select * from hastag; 




