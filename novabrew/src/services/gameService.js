const OLLAMA_URL = 'http://localhost:11434/api/generate';

export async function generateScene(currentScene, lastChoice = null) {
  console.group('🎮 Generating New Scene');
  console.log('Current Scene:', currentScene);
  console.log('Last Choice:', lastChoice);

  const prompt = `Return only valid JSON matching this exact structure:
{
  "scene": {
    "title": "Scene Title",
    "description": "Scene description"
  },
  "choices": [
    {
      "text": "Choice description",
      "healthEffect": number between -20 and 20,
      "manaEffect": number between -20 and 20
    }
  ]
}

Current scene: "${currentScene.description}"
${lastChoice ? `Player chose: ${lastChoice.text}` : ''}

Important: Return ONLY the JSON, no other text.`;

  try {
    const requestBody = {
      model: 'nemotron-mini',
      prompt: prompt,
      stream: false,
      options: {
        temperature: 0.7,
        top_p: 0.9,
        num_predict: 500
      }
    };

    console.log('🌐 Making API Request:', {
      url: OLLAMA_URL,
      method: 'POST',
      body: requestBody
    });

    const response = await fetch(OLLAMA_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    });

    console.log('📥 Response Status:', response.status);

    if (!response.ok) {
      console.error('Response not OK:', await response.text());
      throw new Error(`Ollama API error: ${response.status}`);
    }

    const data = await response.json();
    console.log('📦 Raw API Response:', data);

    try {
      // Clean the response - look for JSON structure
      const jsonMatch = data.response.match(/\{[\s\S]*\}/);
      const jsonString = jsonMatch ? jsonMatch[0] : data.response;
      console.log('🔍 Extracted JSON String:', jsonString);

      const parsedContent = JSON.parse(jsonString + '}'); // Add closing brace if needed
      console.log('✅ Parsed Scene Data:', parsedContent);

      // Validate and normalize the response
      if (!parsedContent.scene || !parsedContent.choices) {
        throw new Error('Invalid response structure');
      }

      // Ensure exactly 3 choices
      while (parsedContent.choices.length < 3) {
        parsedContent.choices.push({
          text: "Explore another path",
          healthEffect: 0,
          manaEffect: 0
        });
      }
      parsedContent.choices = parsedContent.choices.slice(0, 3);

      console.groupEnd();
      return parsedContent;
    } catch (parseError) {
      console.error('❌ JSON Parse Error:', parseError);
      console.log('🔍 Raw response content:', data.response);

      // Fallback response
      const fallback = {
        scene: {
          title: "Continuing the Journey",
          description: "The adventure continues as Sam contemplates their next move."
        },
        choices: [
          { text: "Proceed cautiously", healthEffect: 0, manaEffect: 5 },
          { text: "Take a moment to rest", healthEffect: 5, manaEffect: 0 },
          { text: "Search the surroundings", healthEffect: 0, manaEffect: 0 }
        ]
      };
      console.log('⚠️ Using Fallback Response:', fallback);
      console.groupEnd();
      return fallback;
    }
  } catch (error) {
    console.error('❌ API Error:', error);
    console.groupEnd();
    throw error;
  }
}