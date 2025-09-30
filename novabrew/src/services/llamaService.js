export const LLAMA_URL = 'http://localhost:11434/api/generate';

export async function testLlamaConnection() {
  try {
    const response = await fetch(LLAMA_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'llama3.2',
        prompt: 'Say "test successful" and add more text of your choice make it something random a word or two',
        stream: false
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return {
      success: true,
      response: data.response
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}