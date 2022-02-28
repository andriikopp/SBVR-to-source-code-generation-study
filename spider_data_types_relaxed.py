import nltk
import pandas
import sqlite3
import json

# input SBVR Structured English (SSE) rules

sse_rules = [
    'product owns title',
    'product includes brand',
    'product has description',
    'product has image',
    'product owns price',
    'product owns amount',
    'product includes category',
    'product has votes',
    'product has rating',

    'category owns title',
    'category has description',
    'category has image',

    'brand owns title',
    'brand has image',
    'brand has description',
    'brand owns origin country'
]

# data types learning set preparation

df = pandas.read_json('spider/tables.json')
attributes_support = {}
attributes_confidence = {}
attributes_notnull = []
attributes_pk = []

for (index, row) in df.iterrows():
    db_name = row['db_id']
    table_names = row['table_names']
    conn = sqlite3.connect('spider/database/' +
                           db_name + '/' + db_name + '.sqlite')
    cursor = conn.cursor()

    for table in table_names:
        cursor.execute('PRAGMA table_info(`' + table + '`);')
        query_res = pandas.DataFrame(cursor.fetchall())

        for (index, row) in query_res.iterrows():
            column_name = row[1].lower()
            data_type = row[2].lower()
            not_null = row[3]
            pk = row[5]

            if not_null == 1:
                attributes_notnull.append(column_name)

            if pk == 1:
                attributes_pk.append(column_name)

            if column_name not in attributes_support.keys():
                attributes_support[column_name] = 1
            else:
                attributes_support[column_name] += 1

            if column_name not in attributes_confidence.keys():
                attributes_confidence[column_name] = {data_type: 1}
            else:
                if data_type not in attributes_confidence[column_name].keys():
                    attributes_confidence[column_name][data_type] = 1
                else:
                    attributes_confidence[column_name][data_type] += 1

# calculate association rules

print(attributes_support['phone'])
print(attributes_confidence['phone'])

for column_name in attributes_confidence.keys():
    for data_type in attributes_confidence[column_name].keys():
        attributes_confidence[column_name][data_type] = attributes_confidence[column_name][data_type] / \
            attributes_support[column_name]

# store association rules

association_rules = {}

for col_name in attributes_confidence.keys():
    sorted_by_confidence = sorted(
        attributes_confidence[col_name].items(), key=lambda item: item[1], reverse=True)
    best_type = sorted_by_confidence[0][0]
    best_value = sorted_by_confidence[0][1]
    association_rules[col_name] = {'type': best_type, 'value': best_value}

with open('spider_data_types_relaxed_association_rules.json', 'w') as file:
    json.dump(association_rules, file)

with open('spider_data_types_attributes_notnull.json', 'w') as file:
    json.dump(attributes_notnull, file)

with open('spider_data_types_attributes_unique.json', 'w') as file:
    json.dump(attributes_pk, file)

# rules processing

er_entities = {}
er_relations = {}
er_mandatory = {}

for rule in sse_rules:
    rule = rule.lower()
    tokenized_rule = nltk.word_tokenize(rule)
    tagged_rule = nltk.pos_tag(tokenized_rule)
    _subject = ''
    _predicate = None
    _object = ''

    for item in tagged_rule:
        item_value = item[0]
        item_pos = item[1][:2]

        # parsing criteria

        is_relationship = item_pos == 'VB' and _predicate is None
        is_entity_attribute = item_pos == 'NN' or item_pos != 'VB'
        is_entity = is_entity_attribute and _predicate is None
        is_attribute = is_entity_attribute and _predicate is not None

        if is_entity:
            _subject += ' ' + item_value
        elif is_relationship:
            _predicate = item_value
        elif is_attribute:
            _object += ' ' + item_value

    print(_subject, _predicate, _object)

    if _predicate is not None:
        _subject = _subject.strip().replace(' ', '_')
        _object = _object.strip().replace(' ', '_')

        # process entity attributes

        if _predicate == 'has' or _predicate == 'owns':
            if _subject not in er_entities:
                er_entities[_subject] = {_object: 'text'}
            else:
                er_entities[_subject][_object] = 'text'

            # consider not null attributes

            if _predicate == 'owns':
                if _subject not in er_mandatory:
                    er_mandatory[_subject] = [_object]
                else:
                    er_mandatory[_subject].append(_object)

        # process entity relationships

        if _predicate == 'includes':
            if _subject not in er_relations:
                er_relations[_subject] = [_object]
            else:
                er_relations[_subject].append(_object)

print(er_entities)
print(er_relations)
print(er_mandatory)

# data types suggestion

for _subject in er_entities.keys():
    for _object in er_entities[_subject].keys():
        if _object in attributes_confidence.keys():
            sorted_by_confidence = sorted(
                attributes_confidence[_object].items(), key=lambda item: item[1], reverse=True)
            print(sorted_by_confidence)
            best_match = sorted_by_confidence[0][0]
            best_confidence = sorted_by_confidence[0][1]
            er_entities[_subject][_object] = best_match
            print(_object + ' => ' + best_match +
                  ' (' + str(best_confidence) + ')')


def type(input, lang):
    '''specific data types mapping'''

    generic = {
        'Integer': {'Java': 'Integer', 'CS': 'int', 'SQL': 'int', 'Solidity': 'int'},
        'Floating': {'Java': 'Double', 'CS': 'double', 'SQL': 'real', 'Solidity': 'int'},
        'Boolean': {'Java': 'Boolean', 'CS': 'bool', 'SQL': 'smallint(1)', 'Solidity': 'bool'},
        'String': {'Java': 'String', 'CS': 'string', 'SQL': 'varchar(255)', 'Solidity': 'string'}
    }

    if 'int' in input:
        return generic['Integer'][lang]
    elif 'read' in input or 'double' in input or 'float' in input or 'numeric' in input or 'decimal' in input:
        return generic['Floating'][lang]
    elif 'bool' in input:
        return generic['Boolean'][lang]
    return generic['String'][lang]


# Configuration

lang = ['SQL', 'Java']
dbms = 'MySQL'

# SQL code generation

if 'SQL' in lang:
    output = open('spider_data_types_output.sql', 'w')

    if dbms == 'MySQL':
        # create tables

        for _subject in er_entities.keys():
            output.write('CREATE TABLE `' + _subject + '` (\n')

            # create ids

            output.write('\t`' + _subject +
                         '_id` int NOT NULL AUTO_INCREMENT,\n')

            for _object in er_entities[_subject].keys():
                is_null = 'NULL'

                # check is mandatory fields

                if _subject in er_mandatory.keys() and _object in er_mandatory[_subject]:
                    is_null = 'NOT NULL'

                output.write('\t`' + _object + '` ' +
                             type(er_entities[_subject][_object], 'SQL') + ' ' + is_null + ',\n')

            # create PKs

            output.write('\tPRIMARY KEY (`' + _subject + '_id`)\n')
            output.write(');\n\n')

        # add FKs

        for _subject in er_relations.keys():
            for _object in er_relations[_subject]:
                output.write('ALTER TABLE `' + _subject + '` ADD `' +
                             _object + '_id` int AFTER `' + _subject + '_id`;\n')
                output.write('ALTER TABLE `' + _subject + '` ADD FOREIGN KEY (`' + _object +
                             '_id`) REFERENCES `' + _object + '` (`' + _object + '_id`);\n\n')

    output.close()

# Java code generation

if 'Java' in lang:
    output = open('spider_data_types_output.java', 'w')

    # create tables

    for _subject in er_entities.keys():
        output.write('class ' + _subject + ' {\n')

        for _object in er_entities[_subject].keys():
            attr_type = type(er_entities[_subject][_object], 'Java')
            output.write('\tprivate ' + attr_type + ' ' + _object + ';\n\n')

            # generate setters

            if _subject in er_mandatory.keys() and _object in er_mandatory[_subject]:
                output.write('\tpublic void set_' + _object +
                             '(' + attr_type + ' value) throws Exception {\n')
                output.write('\t\tif (value != null) {\n')
                output.write('\t\t\tthis.' + _object + ' = value;\n')
                output.write('\t\t} else {\n')
                output.write('\t\t\tthrow new Exception("' +
                             _object + ' value is null");\n')
                output.write('\t\t}\n')
            else:
                output.write('\tpublic void set_' + _object +
                             '(' + attr_type + ' value) {\n')
                output.write('\t\tthis.' + _object + ' = value;\n')

            output.write('\t}\n\n')

            # generate getters

            output.write('\tpublic ' + attr_type +
                         ' get_' + _object + '() {\n')
            output.write('\t\treturn this.' + _object + ';\n')
            output.write('\t}\n\n')

        if _subject in er_relations.keys():
            for _object in er_relations[_subject]:

                # generate setters

                output.write('\tprivate ' + _object +
                             ' ' + _object + 'Obj;\n\n')
                output.write('\tpublic void set_' + _object +
                             'Obj(' + _object + ' value) throws Exception {\n')
                output.write('\t\tif (value != null) {\n')
                output.write('\t\t\tthis.' + _object + 'Obj = value;\n')
                output.write('\t\t} else {\n')
                output.write('\t\t\tthrow new Exception("' +
                             _object + ' value is null");\n')
                output.write('\t\t}\n')
                output.write('\t}\n\n')

                # generate getters

                output.write('\tpublic ' + _object +
                             ' get_' + _object + 'Obj() {\n')
                output.write('\t\treturn this.' + _object + 'Obj;\n')
                output.write('\t}\n\n')

        output.write('}\n\n')

    output.close()
