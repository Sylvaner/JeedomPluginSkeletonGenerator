#!/usr/bin/env python

import json
import os
import sys
import shutil

DEFAULT_PACKAGE_NAME = "The best plugin in the world"
DOCUMENTATION_LINK = "https://www.perdu.com"
PHP_CHECK_USER_CONNECT = "" \
    "include_file('core', 'authentification', 'php');\n\n" \
    "if (!isConnect('admin')) {\n" \
    "  throw new Exception('{{401 - Refused access}}');\n" \
    "}\n"
PHP_HEADER = "<?php\n\n"
PHP_INCLUDE_CORE_3 = "" \
    "require_once dirname(__FILE__).'/../../../core/php/core.inc.php';\n\n"
PHP_INCLUDE_CORE_4 = "" \
    "require_once dirname(__FILE__).'/../../../../core/php/core.inc.php';\n\n"
JEEDOM_PLUGIN_CATEGORIES = [
    'security',
    'automation protocol',
    'programming',
    'organization',
    'weather',
    'communication',
    'devicecommunication',
    'multimedia',
    'wellness',
    'monitoring',
    'health',
    'nature',
    'automatisation',
    'energy'
]
ICON = 'iVBORw0KGgoAAAANSUhEUgAAATYAAAFfCAMAAADzmRAJAAAABGdBTUEAALGPC/xhBQAA' \
       'AAFzUkdCAK7OHOkAAABFUExURUdwTJXBK4mvJ420KZTBKpO7KYasIoCjI5XBK5TBKpO+' \
       'KpXBKpK8KZXBKpXBKpS/KpK/KJXBKoy0J462KoaoK4aoKpXBK6eQeXgAAAAWdFJOUwD2' \
       'DiZqGgcB56N9kkPYy1QyuBRgzKxou+CFAAAFhUlEQVR42u3b2VbjRhhF4aMqqX7Nk0Hv' \
       '/6i5CBgwkq0qbHph7X2XqVfydc0iUlJhHPKmmvquK/9kXddPVVMP46xfKox51S1PUznV' \
       'rXu0ma+nbHm++roNDzMb62552srqIXIu75cnr2z8vSdnky1HaGrtjrNzWg5TN9wJbqyW' \
       'Q3UXuLlZDlc//hDN8mw5YtWPjsG+Xw5aOaSr1dly3FIHXDEth65sU9Tacjl6dfyWmi+0' \
       'TJGX/NBgtizL0hdRF9AJsbcFLuIIN/d4vZeNqCW57dxQ5w6reDfHWEuYp4Hd4Pu+cPv5' \
       'skJp5S3p1kWrxmj1/Hb9O0OL0HrN1Yci7qFbna5sB2yi29vp5rZgLGwpy9uIzdVnpI0p' \
       'yu0g5dTLFE2Zpj4D5kb5ChuXqtuXrJmD7n0OvRzZ9uwKF2/kxmDbVcVgu8NdgcGWtLqx' \
       'je4dbp83U49HyhWLj8m76z5+wCHwzLa/j+9YAxgpZxA+u8TcsN4v9IFLfEwDc/Qns5R9' \
       'NG6Wvu2l7KNxjZx100+8JyDimjh+pC9ufLCKzXNqSz258VE5aU9gR0g68PJVObqejTRp' \
       'K+U9PCnH+SPxBMKNNOVWahzbUg5uAYQUNgdCfCfNIMSXqwABNthgg41ggw022GAj2GCD' \
       'DTbYCDbYYIMNNoINNthgg41ggw022GAj2GCDDTbYCDbYYIONYIMNNthgI9hggw022Ag2' \
       '2GCDDTaCDTbYYIONYIMNNthgI9hggw022Ag22GCDDTaCDTbYYCPYYIMNNtgINthggw02' \
       'gg022GCDjWCDDTbYYCPYYIMNNtgINthggw02gg022GCDDTbYYIMNNoINNthgg41ggw02' \
       '2GAj2GCDDTbYCDbYYIMNNoINNthgg41ggw022GAj2GCDDTaCDTbYYIONYIMNNthgI9hg' \
       'gw022Ag22GCDDTaCDTbYYIONYIMNNthgozi2GYT4TnIgpLAFEOIbpAyF6FqpRCG6UepR' \
       'iK6QJhSiC1KDQmylpBqG2HpJAwyxVZI8DPF3K8k4uCUc2ziBxDdLbKXRdRJ7QtqOIJ6O' \
       'UnYEFreUq5U48KYtbVILRUzNG5vxdhTT+MbGESRqjto72wjG/mqd69DYnf9gy9HY2/Sh' \
       'ppnr/N6GT2xsCnsrw2c2Ht3iLlbvVYjsGmzui5ox3GJPH/+7MdziB5skz2YavbKxme67' \
       'V4XvbI4L/a1arcTj+I0qrcZPg1zfD+Z1toJpuvtaxTT92RTlrnB9F3XbbIGPWBtlo67k' \
       'Wd7WO11Tk/EVa7VGN+Khd6XJbrEZH5u/1TvdzLicXm6is3aw8YZ0oVZoV7ilqPGI9GVd' \
       'm7U/9oX3PdQppoHH3mVZliYorpH7wpLlim4+/PNb2Sohq489UadZaY0dEzSlcNgBNxXp' \
       'ajIbD7nClYNMP2s43EzNaqcfZyE/1Fkkawrdp5B3oCUMOIXhEGtcV8+6b+abJ5+rWdWa' \
       'HpC1zyuXTYPTQ9QkycZ6erqjXNY3bdCjszFvpvJZxKq6dfq93Nie8rppqr9Z09T5MM76' \
       '/czMREREREREREREREREO3LFHNaf1YP3X/+ShcJL0un19fX19fy/jZ1f5c0s2PmV/rnf' \
       '6sMmm/PefVWb25MkG15eXl5eTmtsdpRvG8G5jf/Qy3FooWhrJ8nVdZ6fzj8cesxPQG5j' \
       'sMldqJnz7clLMu99MZ9H4iHZLGwMNnPuYrC5wvtCkoVgFg7+nXFrLbLwVcYsOBfCeRUT' \
       'bOt/3uzyj9H65LHJdvF3oRY/Ck0yGYPrN/6po6sdfuaxPKWxgXC/0wYx2P7ehvCcvy3G' \
       'IpC6kdqDf/3nZLv7y8VnqSe9tdrmM1HqpP/yG3FWM0bb9SkZgpvX2Ay27V8ruNl7/31p' \
       '45hzY38JIYR/9S/wH0cYwKgtpTePAAAAAElFTkSuQmCC'


def ask_y_n(question, default='y'):
    """Ask a question whose answer is yes or no.

    :param question: Question to display
    :param default:  Default answer (y or n). y by default.
    :type question:  str
    :type default:   str
    :return:         User answer
    :rtype:          str
    """
    choices = 'Y/n'
    if default != 'y':
        choices = 'y/N'
    choice = raw_input('%s [%s] : ' % (question, choices)).lower()
    if choice == default or choice == '':
        return default
    return choice


def ask_with_default(message, default):
    """Ask for user input with a default value is user hit enter.abs

    :param message: Message to display
    :param default: Default answer
    :type message:  str
    :type default:  str
    :return:        User answer
    :rtype:         str
    """
    answer = raw_input('%s [%s] : ' % (message, default))
    if answer == '':
        answer = default
    return answer


def ask_with_multiple_choices(message, choices):
    """Ask for a multiple choice

    :param message: Message to display
    :param choices: Choices
    :type message:  str
    :type default:  list
    :return:        User choice
    :rtype:         int
    """

    print(message+' : ')
    for index, choice in enumerate(choices):
        print(' '+str(index + 1)+'. '+choice)

    loop = True
    while loop:
        choice = raw_input("Choice : ")
        result = 0
        try:
            result = int(choice)
        except ValueError:
            pass
        if result > 0 and result <= len(choices):
            loop = False

    return choices[result - 1]


def create_folder_struct(plugin_id):
    """Create all the necessary folders.

    :param plugin_id: Id of the plugin_id
    :type plugin_id: str
    """
    subfolders = [
        '3rdparty',
        'core',
        'desktop',
        'docs',
        'plugin_info',
        'ressources'
    ]
    core_subfolders = [
        'ajax',
        'class',
        'php',
        'template'
    ]
    desktop_subfolders = [
        'css',
        'js',
        'modal',
        'php'
    ]
    # Parent folder
    os.mkdir(plugin_id)
    # First level subfolders
    for subfolder in subfolders:
        os.mkdir(plugin_id+os.sep+subfolder)
    # Desktop subfolders
    for desktop_subfolder in desktop_subfolders:
        os.mkdir(plugin_id+os.sep+'desktop'+os.sep+desktop_subfolder)
    # Core subfolders
    for core_subfolder in core_subfolders:
        os.mkdir(plugin_id+os.sep+'core'+os.sep+core_subfolder)
    # license file
    license_file = open(plugin_id+os.sep+'LICENSE', 'w')
    license_file.close()
    # Documentation folder
    os.mkdir(plugin_id+os.sep+'docs'+data['documentation_language'])


def get_data():
    """Get data about the future plugin.
    :return: Asked data
    :rtype:  dict
    """
    data = {}

    print(' - The name is a string that will be display in Jeedom interface')
    data['name'] = ask_with_default('Name : ', DEFAULT_PACKAGE_NAME)
    plugin_id = data['name'].lower().replace(' ', '_')

    print(' - The ID is a uniq string that identified your plugin.')
    plugin_id = data['id'] = ask_with_default('ID : ', plugin_id)
    data['description'] = raw_input('Description (optional) : ')
    data['license'] = ask_with_default('License', 'GPL')
    data['author'] = raw_input('Author (optionnal) : ')
    data['require'] = ask_with_default('Jeedom required version', '3.0')
    data['version'] = ask_with_default('Plugin version', '1.0')
    data['category'] = ask_with_multiple_choices(
            'Plugin category', JEEDOM_PLUGIN_CATEGORIES)
    data['documentation_language'] = ask_with_default(
            'Documentation language (fr_FR, en_US)', 'en_US')

    configuration = None

    if ask_y_n('Generate plugin configuration page ?'):
        configuration = {}
        loop = True
        item_type = {
            'Text input': 'text',
            'Checkbox': 'checkbox',
            'No': 'stop'
            }
        while loop:
            result = ask_with_multiple_choices('Add field ?', item_type.keys())
            field_type = item_type[result]
            if field_type == 'stop':
                loop = False
            else:
                label = raw_input('Label : ')
                code = raw_input('Code : ')
                configuration[field_type] = {'label': label, 'code': code}
    data['configuration'] = configuration

    # Generate shortcuts
    data['plugin_info_path'] = plugin_id+os.sep+'plugin_info'+os.sep
    data['core_path'] = plugin_id+os.sep+'core'+os.sep
    data['desktop_path'] = plugin_id+os.sep+'desktop'+os.sep

    return data


def gen_info_json(data):
    """Write info.json file in plugin_info directory.
    This file contains general data of the plugin.

    :param data: All data
    :type data: dict
    """
    with open(data['plugin_info_path']+'info.json', 'w') as dest:
        dest.write(
                   '{\n'
                   '  "id" : "%s",\n'
                   '  "name": "%s",\n'
                   '  "licence": "%s",\n'
                   '  "require": "%s",\n'
                   '  "version": "%s",\n'
                   '  "category": "%s",\n'
                   '  "hasDependency": false,\n'
                   '  "hasOwnDaemon": false,\n'
                   '  "maxDependancyInstallTime": 0,\n'
                   '  "documentation": "%s",\n'
                   '  "changelog": "%s"' % (
                       data['id'],
                       data['name'],
                       data['license'],
                       data['require'],
                       data['version'],
                       data['category'],
                       DOCUMENTATION_LINK,
                       DOCUMENTATION_LINK
                       )
                   )
        if data['description'] != '':
            dest.write(',\n  "description": "%s"' % data['description'])
        if data['author'] != '':
            dest.write(',\n  "author": "%s"' % data['author'])
        dest.write('\n}\n')
        dest.close()


def gen_icon(data):
    """Write plugin icon file plugin_info directory.

    :param data: All data
    :type data: dict
    """
    with open(data['plugin_info_path']+data['id']+'_icon.png', 'wb') as dest:
        dest.write(ICON.decode('base64'))
        dest.close()


def gen_installation_php(data):
    """Write installation.php file in plugin_info directory.
    This file contains functions called when plugin is installed, updated or
    removed.

    :param data: All data
    :type data: dict
    """
    funcs = ['install', 'update', 'remove']

    with open(data['plugin_info_path']+'installation.php', 'w') as dest:
        dest.write(PHP_HEADER+PHP_INCLUDE_CORE_3)
        for func in funcs:
            dest.write('function '+data['id']+'_'+func+'() {\n\n}\n\n')
        dest.close()


def gen_configuration(data):
    """Write configuration.php file in plugin_info directory.
    This file contains all plugin configuration fields.

    :param data: All data
    :type data: dict
    """
    with open(data['plugin_info_path']+'configuration.php', 'w') as dest:
        dest.write(PHP_HEADER+PHP_INCLUDE_CORE_3+PHP_CHECK_USER_CONNECT+"?>\n")
        dest.write('<form class="form-horizontal">\n  <fieldset>\n')
        if data is not False:
            for field_type, field_data in data['configuration'].items():
                dest.write('    <div class="form-group">\n'
                           '      <label class="col-sm-3 control-label">\n'
                           '        {{%s}}\n'
                           '      </label>\n'
                           '      <div class="col-sm-9">\n'
                           '        <input class="configKey form-control" '
                           '' % (field_data['label']))
                if (field_type == 'checkbox'):
                    dest.write('type="checkbox" ')
                dest.write('data-l1key="%s" />\n'
                           '      </div>'
                           '    </div>'
                           '' % (field_data['code']))
        dest.write('  </fieldset>\n</form>\n')
        dest.close()


def gen_desktop_php(data):
    """Write PHP desktop render in desktop directory.
    This file contains the desktop view of the plugin.

    :param data: All data
    :type data: dict
    """
    with open(data['desktop_path']+'php'+os.sep+data['id']+'.php',
              'w') as dest:
        dest.write('<?php\n')
        dest.write(PHP_CHECK_USER_CONNECT+"?>\n")
        dest.close()


def gen_core_php(data):
    """Write PHP engine file in core directory.
    This file is the principal file of the plugin.
    They are two class : plugin_id and plugin_idCmd

    :param data: All data
    :type data: dict
    """
    with open(data['core_path']+'class'+os.sep+data['id']+'.class.php',
              'w') as dest:
        dest.write(PHP_HEADER+PHP_INCLUDE_CORE_4)
        dest.write(''
                   'class %s extends eqLogic {\n\n'
                   '  /*************** Attributs ***************/\n\n'
                   '  /************* Static methods ************/\n\n'
                   '  /**************** Methods ****************/\n\n'
                   '  /********** Getters and setters **********/\n\n'
                   '}\n\n'
                   'class %sCmd extends cmd {\n\n'
                   '  /*************** Attributs ***************/\n\n'
                   '  /************* Static methods ************/\n\n'
                   '  /**************** Methods ****************/\n\n'
                   '  /********** Getters and setters **********/\n\n'
                   '}\n' % (data['id'], data['id']))
        dest.close()


def save_data(data):
    """Save data in json file for next launch.

    :param data: All data
    :type data: dict
    """
    with open('data.json', "w") as dest:
        json.dump(data, dest)
        dest.close()


# Entry point
if __name__ == '__main__':
    config_loaded_from_file = None
    # Read CLI args and load data from file is data.json exists
    data = None
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            config_file = open(sys.argv[1])
            data = json.load(config_file)
            config_file.close()
            config_loaded_from_file = True

    # Ask user for data
    if data is None:
        data = get_data()
        config_loaded_from_file = False

    target = data['id']
    # Tests if the plugin folder already exists and ask for deletion
    if os.path.exists(target):
        print('Directory "'+target+'" already exists.')
        if ask_y_n('Do you want to delete it ?') == 'y':
            shutil.rmtree(target)
        else:
            print('Process aborded.')
            exit()

    # Start the generation
    create_folder_struct(target)

    gen_info_json(data)
    gen_icon(data)
    gen_installation_php(data)
    gen_configuration(data)
    gen_desktop_php(data)
    gen_core_php(data)

    # Save data into file
    if not config_loaded_from_file:
        if ask_y_n("Do you want to save this data ?") == 'y':
            save_data(data)
            print("To regenerate this : "+sys.argv[0]+" data.json")
