# Biblia AI Chat API
## A REST API to chat with Bible characters using AI

(SwaggerUI Documentation)[https://api-bible-ai.onrender.com/docs]

- This API uses `DeepSeek-r-1(free)` model through `openrouter` which allows access to `300+ LLMs` in one platform.

### Idea and Concept
- I thought about doing this project through my day to day interactions with kids. Kids ask alot of questions and they are always curious to know and learn. My relatives always ask me to tell them stories from the Bible about how God worked with different people in the Bible and what lesson can they take from it. I enjoy every minute narrating these stories because i feel like there is no other stories greater written than the ones in the Bible (personal opinion). <br>

- Then i realised that what if am not around who is going to narrate these stories to them. Then an idea came, `What if there is an AI app like Whatsapp where kids select a character from the list of AI generated Bible characters and chat with with them and let them narrate their own stories themselves`, then this happened.

### Design and development
- The API is in `version 1.0.0` phase one of its design and development with Minimal Viable features (MVP), with the following features;
    - User registers and login in
    - User manages their profile(Reset passwords)
    - Select Bible Character to chat with eg. David, King Solomon
    - Chat with the character with AI generated responses
    - User deletes messages
    - User deletes the whole chat with the character
    - Search for a character on the list

- I did not want to complicate things for the first version. I felt like these features are good for the MVP.to make it simple and easy to use.

- I have used the `Model View Controller (MVC)` with a `REST-ful` approach to design the API endpoints which i found easy to understand and implement.

- Tools used in this project include; 
    - `Python Flask` framework for routing and configurations
    - `PostgreSQL` a relational database store all the data (chats and user details)
    - `JWT` for user authentication
    - `Visual Studio Code` the best code editor in the world (personal opinion)
    - `git and github` for version control and repo hosting
    - `EchoAPI` a free VS Code extension for testing API endpoints (my favorite)
    - `SwaggerUI` for API endpoints documentation
    - `DeepSeek-r-1(free)` AI assistant API for text response generation

- I know there are alot of tools out there which can make this project even better, these are just personal opinions from my knowledge and experience.

### Lessons and challenges
- I had fun buiding this project. I encountered several challenges but i was happy to seeing the errors overcome through endless research and debugging, thats what we do in this field.

- I have learnt how to integrate AI API in projects and how to fine tune an AI model to generate the required responses, this was amazing to seeing it come to pass.

### Post MVP
- Am still building this API and will add some features are i build into the second phase.

- If you are interested in this project you are free to use this repo and/or contribute more to it, i mean why not.

> Happy coding!