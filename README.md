# testrattingcapitals.com

A quick and dirty digital Wall of Shame for the EVE group TEST Alliance Please Ignore.

Reads in the latest of specific types of ship losses, and renders how long ago they were, and a link to the most recent kill

Built in react/redux, with a simple node script to run in cron to update.

## Prerequisites.

* Node 6.9+
* yarn, gulp, babel, webpack
  * `npm install -g yarn gulp babel-cli webpack`

## Build

1. ``yarn``
2. ``yarn start``

Web client lands in _/dist_, server script lands in _/lib/server_.

## Run (production)

* Build
* dump the contents of _/dist_ into your web server root
* add a crontab entry to run the serverside script at the interval of your choice. Redirect stdout to your _/webserver_root/data.json_
