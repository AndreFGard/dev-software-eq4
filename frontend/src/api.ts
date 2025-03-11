export const apiUrl= import.meta.env.VITE_API_URL

export interface Message{
    username: string;
    content:string;
    is_activity?:boolean;
    id?:Number;
}

export async function addMessage(msg: Message){
    const response = await fetch(`${apiUrl}/addMessage`, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify(msg),
    })
    console.log(response);
    return response.json()
}

export async function getMessages(username: string): Promise<Message[]>{
    const response = await fetch(`${apiUrl}/getMessages?username=${encodeURIComponent(username)}`, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        }
    })
    console.log(response);
    return response.json()
}

export async function addToFavoritesBack(username:string, msg: Message){
    const response = await fetch(`${apiUrl}/addToFavorites`, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({username: username, msg: msg}),
    })
    return response.json()
}

export async function getFavorites(username: string): Promise<Message[]>{
    const response = await fetch(`${apiUrl}/getFavorites?username=${encodeURIComponent(username)}`, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        }
    })
    return response.json()
}

export async function removeFromFavoritesBack(username, msg) {
    await fetch(`${apiUrl}/removeFavorite`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, content: msg.content }),
    });
  }
  