# Sky-Chatting-Room

## Introduce

Chatting Room with Socket / MultiThread / Tkinter.

A little demo in socket, solving the following problems:

1. stick pack and unpacking in TCP

2. AES Encrypt

3. Long-time Link

4. Reader-Writer Model in Threading Management

## 收发数据交互格式:

`{'type': type, 'author': author, 'content': content}`

type: <string>\[`command`|`message`\]

author: <string> name of the poster

content:<string>

  command: \[`quit`|`keeper`|`keep`\]
  
   - `quit`: When you quit the client, send the message to quit the link.
   
   - `keeper`: The server protection thread sends the message to keep the link.
   
   - `keep`: If you want to keep the long link, send the message.
   
  message: content-value