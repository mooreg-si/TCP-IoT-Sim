# TCP IoT Simulator

A basic Python TCP server to simulate an IoT device communicating over TCP with a control system. This was created primarily to help test Q-SYS plugins during development but is not specific to Q-SYS and could also be useful with other control systems. The simulator will allow verification of messages received from the control system through standard python debugging tools or the printed messages. Command/response pairs are loaded from a JSON file. When a message is received from the client, it is checked for a match in the JSON file. If there is a matching command, the corresponding response is sent back to the client. The command/response table can be created following the example based on documentation from the device manufacturer. Authentication can also be simulated

## Configuration

Configuration is through a config.json file in the root folder. This file should not be included in version control if using authentication.

| Variable             | Purpose                                                                                                   |
| -------------------- | --------------------------------------------------------------------------------------------------------- |
| host                 | The IP address that this server should listen on.                                                         |
| port                 | The communication port that the server should listen on.                                                  |
| commandPairs         | The path to the file to use for the command response pairs                                                |
| stateVariable        | The character used to identify state variables within a command or response                               |
| authRequired         | If authentication is required for this device                                                             |
| passwordString       | The password string**RECEIVED FROM THE CONTROL SYSTEM** in response to a request for authentication |
| authSuccess          | The string sent**FROM THE SERVER** to request authentication                                       |
| unauthorizedResponse | The string sent**FROM THE SERVER** in response to a message without authentication                 |

## State Variables

State variables can be used to store a value sent by the client and repeat it back later. This also allows for command messages that include a state without using multiple messages for each possible state. For example, if a command is sent to turn a display on, later status requests should report that display on. If a command is sent to switch the input to HDMI3, later status requests should report the current input as HDMI3.

### State Variables in Messages

State variables in command messages take the form `#01`. The first `#` character is the configured stateVariable character and identifies the location of the variable in the string. The second integer character is the index of the state variable and can be 0-9. The third integer character is the length of the variable, and can be 1-9. For the received command message `POWR01\r`, the message string stored in the command response table would be `POWR0#01\r`.

### State Variables in Responses

State variables in responses take the form `#0`. The first `#` character is the configured stateVariable character and identifies the location of the variable in the string. The second integer character is the index of the state variable and can be 0-9. To send the response message `POWR01\r`, the message string stored in the command response table would be `POWR0#0\r`.

## Command Tables

Commands and responses must be provided exactly as they would be sent and received between the control system and the device being simulated, including all non-printable characters, such as carriage returns and newline characters. Non-printable characters must be properly escaped.

### Common non-printable characters

| Name            | HEX | JSON Char |
| --------------- | --- | --------- |
| Carriage Return | 0D  | \r        |
| New line        | 0A  | `\l`    |
| Escape          | 1B  | \\\u001b  |
