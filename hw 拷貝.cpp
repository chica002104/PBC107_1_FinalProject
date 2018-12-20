#include <iostream>
#include <cstring>
#include <iomanip>
#include <stdexcept>
using namespace std;
const int MAX_ENTRY = 200; //maximun number of entries allowed
const int MAX_FIELD = 20;  //maximun number of fields allowed
const int MAX_TABLE = 10;  //maximun tables allowed in a database
const int MAX_STRING_LEN = 10;  //maximun length of string in data allowed (include field name)
const int MAX_LINE_LEN = 300; 
struct Field 
{
	char* name;
	char** data;
};
struct Command 
{
	int selectNum;
	char** select; //select
	char* tableName;	 //from
};
class Table 
{
private:
	char* tableName;
	int numOfField;
	int numOfEntry;
	Field* field;
	Field* getField(char* name) 
	{
		for (int i = 0; i < numOfField; ++i)
		{
			if (strcmp(name, field[i].name) == 0)
			{
				return &field[i];
			}
		}
		return nullptr;
	}
	
public:
	Table(char name[]) 
	{
		int len = strlen(name);
		tableName = new char[len + 1];
		strcpy(tableName, name);
		field = new Field[MAX_FIELD];
		numOfField = 0;
		numOfEntry = 0;
	}
	void print() 
	{
		if (numOfEntry == 0 || numOfField == 0)
		{
			cout << "Empty set\n";
			return;
		}
		int* tabSize = new int[numOfField];
		int totalTabSize = 0;
		for (int i = 0; i < numOfField; ++i)
		{
			tabSize[i] = 0;

			for (int j = 0; j < numOfEntry; ++j)
			{
				int len = strlen(field[i].data[j]);
				if (len > tabSize[i])
				{
					tabSize[i] = len;
				}
			}
			if (strlen(field[i].name) > tabSize[i])
			{
				tabSize[i] = strlen(field[i].name);
			}
			tabSize[i] += 1;
			totalTabSize += tabSize[i];
		}
		int lenOfSeperationLine = totalTabSize + 3*numOfField + 2;
		char* seperationLine = new char[lenOfSeperationLine];
		for (int i = 0; i < lenOfSeperationLine; ++i)
		{
			seperationLine[i] = '-';
		}
		seperationLine[lenOfSeperationLine - 1] = 0;

		cout << seperationLine << "\n";

		cout << "|";
		for (int i = 0; i < numOfField; ++i)
		{
			cout <<" "<<left<< setw(tabSize[i]) << field[i].name  << " |";
		}

		cout <<"\n"<< seperationLine << "\n";
		for (int i = 0; i < numOfEntry; ++i)
		{
			cout << "|";
			for (int j = 0; j < numOfField; ++j)
			{
				cout <<" "<< left << setw(tabSize[j]) << field[j].data[i] << " |";
			
			}
			cout << "\n";
		}
		cout << seperationLine << "\n";
		if (numOfEntry > 1)
		{
			cout << numOfEntry << " rows in set\n";
		}
		else
			cout << "1 row in set\n";
		
		
		delete [] tabSize;
		delete [] seperationLine;
	}
	bool addField(char* colName) /*TODO*/
	{
		if (numOfField >= MAX_FIELD)
		{
			return false;
		}
		field[numOfField].name = new char[strlen(colName) + 1];
		strcpy(field[numOfField].name, colName);
		field[numOfField].data = new char*[MAX_ENTRY];

		numOfField ++;
		return true;
	}
	bool addEntry(char** data) /* TODO */
	{
		if (numOfEntry >= MAX_ENTRY)
		{
			return false;
		}
		for (int i = 0; i < numOfField; ++i)
		{
			field[i].data[numOfEntry] = new char[MAX_STRING_LEN];
			strcpy(field[i].data[numOfEntry], data[i]);

		}
		numOfEntry ++;
		return true;
	}
	bool loadcsv(char fileName[]) /* GIVEN or TODO */
	{
		// cout << "loading file "<<fileName<<"\n";
		FILE* csvFile = fopen(fileName, "r");
		if (csvFile == nullptr)
		{
			fprintf(stderr, "open file error\n");
			return false;
		}
		char* line = new char[MAX_LINE_LEN];
		int entryIndex = 0;

		
		for (int i = 0; i < MAX_FIELD; ++i)
		{
			field[i].data = new char*[MAX_ENTRY];
		}
		int fieldIndex = 0;
		if (fgets(line, MAX_LINE_LEN, csvFile))
		{
			char* token = strtok(line, ",;\n");
			
			while(token != nullptr)
			{
				field[fieldIndex].name = new char[MAX_STRING_LEN];
				strcpy(field[fieldIndex].name, token);

				fieldIndex++;
				token = strtok(nullptr, ",;\n");
			}
		}
		else{

			fprintf(stderr, "input file empty\n");
			return false;
		}
		numOfField = fieldIndex;

		bool typeDecided = false;
		while(fgets(line, MAX_LINE_LEN, csvFile))
		{
			char* token = strtok(line, ",\n");
			int fieldIndex = 0;
			
			while(token != nullptr)
			{
				field[fieldIndex].data[entryIndex] = new char[MAX_STRING_LEN];
				strcpy(field[fieldIndex].data[entryIndex], token);
						
				token = strtok(nullptr, ",\n");
				fieldIndex ++;
			}
			entryIndex ++;
		}
		numOfEntry = entryIndex;

	}
	Table* executeCmd(Command cmd) /* TODO */
	{
		char resultTableName[100] = "result";
		Table* result = new Table(resultTableName);
		bool* fSelected = new bool[numOfField];
		if (cmd.selectNum == 1 && strcmp(cmd.select[0], "*") == 0) //select *
		{
			cmd.selectNum = numOfField;
			for (int i = 0; i < numOfField; ++i)
			{
				fSelected[i] = true;
				result->addField(field[i].name);
			}
		}
		else
		{
			for (int i = 0; i < numOfField; ++i)
			{
				fSelected[i] = false;
				for (int j = 0; j < cmd.selectNum; ++j)
				{
					if (strcmp(cmd.select[j], field[i].name) == 0) 
					{
						fSelected[i] = true;
						result->addField(field[i].name);
					}
				}
			}
		}
		
		char** entry = new char*[cmd.selectNum];
		Field* conditionField = nullptr;
		int entryIndex = 0;
		while(entryIndex < numOfEntry)
		{

			int fieldIndex = 0;
			for (int i = 0; i < numOfField; ++i)
			{
				if (fSelected[i])
				{
					entry[fieldIndex] = field[i].data[entryIndex];
					fieldIndex ++;
				}
			}
			result->addEntry(entry);
			entryIndex++;
		}
		delete [] fSelected;
		delete [] entry;
		return result;
	}
	char* getName() 
	{
		return tableName;
	}
	~Table() 
	{
		delete [] field;
		delete [] tableName;
	}
	
};
class Database
{
private:
	int numOfTables;
	Table** tables; 
public:
	Database() 
	{
		numOfTables = 0;
		tables = nullptr;
	}
	bool newTable(Table* table) /* TODO */
	{
		if (tables == nullptr)
		{
			tables = new Table*[MAX_TABLE];
		}
		if (numOfTables >= MAX_TABLE)
		{
			return false;
		}
		tables[numOfTables] = table;
		numOfTables ++;
		return true;
	}
	Table* executeCmd(Command cmd) 
	{
		for (int i = 0; i < numOfTables; ++i)
		{
			if (strcmp(cmd.tableName, tables[i]->getName()) == 0)
			{
				return tables[i]->executeCmd(cmd);
			}
		}
		char tableName[10] = "result";
		Table* emptyTable = new Table(tableName);
		return emptyTable;
	}
	~Database() 
	{
		for (int i = 0; i < numOfTables; ++i)
		{
			delete tables[i];
		}
		delete [] tables;
	}
	
};
Command parseCommand(char command[]) /* TODO */
{
	char** token = new char*[MAX_FIELD + 20];
	int numOfToken = 0;
	token[numOfToken] = strtok(command, ",; \n");
	while(token[numOfToken] != nullptr)
	{
		numOfToken ++;
		token[numOfToken] = strtok(nullptr, ",; \n");
	}
	
	Command cmd;
	cmd.select = &token[1];
	for (int i = 2; i < numOfToken; ++i)
	{
		if (strcmp(token[i], "FROM") == 0)
		{
			cmd.tableName = token[i + 1];
			cmd.selectNum = i - 1;
			break;
		}
	}
		

	return cmd;
}
int main(int argc, char const *argv[])
{
	//data imput from terminal
	setvbuf(stdout, nullptr, _IONBF, 0);
	Database db;
	int numOfTables = 0;
	cin >> numOfTables;
	for (int i = 0; i < numOfTables; ++i)
	{
		char* tableName = new char[100];
		cin >> tableName;
		char* fileName = new char[100];
		cin >> fileName;
		Table* t = new Table(tableName);
		t->loadcsv(fileName);
		db.newTable(t);
	}
	char command[300];
	cin.getline(command, 300);
	cin.getline(command, 300);
	Command cmd = parseCommand(command);
	// printCmd(cmd);
	Table* result = db.executeCmd(cmd);
	result->print();
	

	return 0;
}