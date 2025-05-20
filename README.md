# TCP IoT Simulator

A basic Python TCP server to simulate an IoT device communicating over TCP with a control system. This was created primarily to help test Q-SYS plugins during development but is not specific to Q-SYS and could also be useful with other control systems. The simulator will allow verification of messages received from the control system through standard python debugging tools or the printed messages. Command/response pairs are loaded from a JSON file. When a message is received from the client, it is checked for a match in the JSON file. If there is a matching command, the corresponding response is sent back to the client. The command/response table can be created following the example based on documentation from the device manufacturer. Authentication can also be simulated

## Configuration

Configuration is through a config.json file in the root folder. This file should not be included in version control if using authentication.

| Variable             | Purpose                                                                                                   |
| -------------------- | --------------------------------------------------------------------------------------------------------- |
| host                 | The IP address that this server should listen on.                                                         |
| port                 | The communication port that the server should listen on.                                                  |
| commandPairs         | The path to the file to use for the command response pairs                                                |
| wc-fixed             | The wildcard character to use for a single character (not implemented yet)                                |
| wc-variable          | The wildcard character to use for a variable length group of characters (not implemented yet)             |
| authRequired         | If authentication is required for this device                                                             |
| passwordString       | The password string**RECEIVED FROM THE CONTROL SYSTEM** in response to a request for authentication |
| authSuccess          | The string sent**FROM THE SERVER** to request authentication                                       |
| unauthorizedResponse | The string sent**FROM THE SERVER** in response to a message without authentication                 |

## Command Tables

Commands and responses must be provided exactly as they would be sent and received between the control system and the device being simulated, including all non-printable characters, such as carriage returns and newline characters. Non-printable characters must be properly escaped.

### Common non-printable characters

| Name            | HEX | JSON Char |
| --------------- | --- | --------- |
| Carriage Return | 0D  | \r        |
| New line        | 0A  | `\l`    |
| Escape          | 1B  | \\\u001b  |
