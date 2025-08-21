⚡ Dynamic Tool Filtering in OpenAI Agents SDK
❓ Dynamic Tool Filtering Kya Hai?
---
Dynamic tool filtering ka matlab hai ke aap apne agent ko dene waali tools ki list ko run-time par control kar sakte hain.

Matlab: Aap ek function likhte hain jo decide karta hai ke is waqt agent ke liye konsi tools available honi chahiye aur konsi nahi.

Ye ek “smart menu” ki tarah hai:

Subah → breakfast menu

Raat → dinner menu

Bilkul isi tarah, agent ka tool menu bhi context ke hisaab se change hota hai.

🔑 Ye Zaroori Kyun Hai?
---
🧠 Context-aware control
---
Agent ko uske kaam ke mutabiq tools milte hain.

Example: Agar agent sirf mood-related kaam kar raha hai → sirf mood tools show hongi.
---
🔒 Behtar Security
---
Aap decide karte ho kon user/agent kis tool ko access kar sakta hai.

Sensitive tools ko hide kiya jaa sakta hai.

⚡ Flexibility
---
Static filtering mein → ek baar jo tools allow kar diye, wahi fix rahte hain.

Dynamic filtering mein → tools ki list conditions ke hisaab se change hoti hai.
---
⚙️ Ye Kaam Kaise Karta Hai?
1️⃣ Ek Filter Function Banayein
---
Filter function do cheezen leta hai:

ToolFilterContext → agent aur server ki info deta hai.

tool → har tool ke details.

Function return karega:

True → Tool available hogi

False → Tool hide kar di jayegi
---
2️⃣ Example Logics
🔹 Simple Logic
return tool.name.startswith("mood")


👉 Sirf woh tools show hongi jo "mood" se shuru hoti hain.
---
🔹 Context-aware Logic
return context.agent.name == "MyMCPConnectedAssistant" and tool.name == "mood_from_shared_server"


👉 Agar agent ka naam "MyMCPConnectedAssistant" hai, tab sirf "mood_from_shared_server" tool show hogi.
---
🔹 Async Logic

Aap async function bhi bana sakte ho → kisi API ya database check ke basis par decide karne ke liye.
---
3️⃣ MCP Server Client Mein Use Karein
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from agents.mcp.types import ToolFilterContext

# Apna filter function
def custom_filter(context: ToolFilterContext, tool) -> bool:
    # Example logic: sirf mood wali tools show karo
    return tool.name.startswith("mood")

mcp_params = MCPServerStreamableHttpParams(url="http://localhost:8001/mcp/")

async with MCPServerStreamableHttp(
    params=mcp_params,
    tool_filter=custom_filter,
    name="MyDynamicMCPServer"
) as mcp_server_client:
    # Ab agent run karein, woh sirf mood wali tools use kar payega
    pass
---
🎯 Final Result
---
Dynamic tool filtering agent ko:

Smarter banata hai 🧠

Secure banata hai 🔒

Fine-grained control deta hai ⚙️

👉 Isse aap apne agent ki abilities ko specific task aur situation ke hisaab se customize kar sakte ho.
