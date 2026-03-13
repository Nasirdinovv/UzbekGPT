from API_KEY import API_KEY
from google import genai

client = genai.Client(api_key=API_KEY)

def chat_agent(role = "oddiy suhbatdosh", message = "Sen nimalar gila olasan?"):

    contents = f"""

        SEN BU ROLDAGI {role} PROFESSIONAL SUXBATDOSHSAN. fagat shu mavzudagi savollarga javob gaytarasan

        agar boshqa mavzuda savol berishsa 'Uzr men bu mavzuda gaplasha olmayman

        seni javobing uzunligi har doim eng ko'p bilan 200 ta so'zdan iborat bo'lsin. Fagat mavzu bo'yicha berilgan savolga javob gaytar.
        savol: {message}

        Javob har doim oddiy text bo'lsin

    """

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=contents
    )
    return response.text

