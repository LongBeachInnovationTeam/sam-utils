# sam-postgres-import

## About

This repository contains the **collections.yml** file required by [mosql](https://github.com/stripe/mosql) gem. **collections.yml** is a database-to-database mapping file written in YAML. mosql will continously import the **contacts** and **locations** collections form mongodb into tables in postgresql.

## Usage

You can run mosql in the foreground by running the following on the command line:

    $ mosql --sql postgres://$USERNAME:$PASSWORD@localhost:5432/sam_contacts --mongo mongodb://localhost:27017/sam-contacts

If you need to re-import the table, you can mosql with the `--reimport` option:

    $ mosql --sql postgres://$USERNAME:$PASSWORD@localhost:5432/sam_contacts --mongo mongodb://localhost:27017/sam-contacts --reimport


## Installation

*These instructions have only been tested on a fresh Ubuntu 14.04 instance. YMMV.*

If you do not already have ruby installed on the server, you must install the following ruby dependencies:

	sudo apt-get update
	sudo apt-get install git-core curl zlib1g-dev build-essential libssl-dev libreadline-dev libyaml-dev libsqlite3-dev sqlite3 libxml2-dev libxslt1-dev libcurl4-openssl-dev python-software-properties libffi-dev

Ruby then can be installed with rbenv (latest version of ruby at the time of writing is v2.2.3):

	cd
	git clone git://github.com/sstephenson/rbenv.git .rbenv
	echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
	echo 'eval "$(rbenv init -)"' >> ~/.bashrc
	exec $SHELL

	git clone git://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
	echo 'export PATH="$HOME/.rbenv/plugins/ruby-build/bin:$PATH"' >> ~/.bashrc
	exec $SHELL

	git clone https://github.com/sstephenson/rbenv-gem-rehash.git ~/.rbenv/plugins/rbenv-gem-rehash

	rbenv install 2.2.3
	rbenv global 2.2.3
	ruby -v

If you do not have postgresql-server-dev-X.Y for building a server-side extension or libpq-dev for building a client-side applications, install the following from the command line:

    $ sudo apt-get install -y postgis postgresql-9.3-postgis-2.1
    $ sudo apt-get install libpq-dev

Finally, install mosql from Rubygems:

    $ gem install mosql