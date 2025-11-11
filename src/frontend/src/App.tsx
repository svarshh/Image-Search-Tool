import './App.css'

const API_URL = 'http://127.0.0.1:8000';

async function get_files(word:string): Promise<string>{
  const response = await fetch(`${API_URL}/api/data/${word}`);
  if(!response.ok){
    throw new Error("Failed fetch");
  }
  console.log(response)
  return await response.json();
}
async function post_dir(path_name: string){
  const response = await fetch(`${API_URL}/api/submit`,{
  method: 'POST',
  headers: {
    'Content-Type' : 'application/json',
  },
  body: JSON.stringify(path_name)
  });
  if(!response.ok){
    throw new Error("Failed post");
  }
  return response.json();
}

const PostData: React.FormEventHandler<HTMLFormElement> = async (event: React.FormEvent<HTMLFormElement>) => {
  event.preventDefault(); 
  const form = event.currentTarget;
  const path_name = form.elements.namedItem('path_name') as HTMLInputElement;
  try {
    await post_dir(path_name.value); 
    console.log("Form submitted successfully!");
  } catch (error) {
    console.error("Error during form submission:", error);
  }
};

const GetData: React.FormEventHandler<HTMLFormElement> = async (event: React.FormEvent<HTMLFormElement>) => {
  event.preventDefault(); 
  const form = event.currentTarget;
  const word = form.elements.namedItem('word') as HTMLInputElement;
  try {
    const response = await get_files(word.value); 
    console.log("Form retrieed successfully!");
    console.log(response);
  } catch (error) {
    console.error("Error during form submission:", error);
  } 
};

function App() {
  return (
    <>
      <div>
        <form onSubmit={PostData}>
          <label>
            Enter Folder Path:  
            <br></br>
            <input type="text" name="path_name" required/>
          </label>
          <br></br>
        
          <button type="submit">
            Submit
          </button>
        </form>

         <form onSubmit={GetData}>
          <label>
            Enter Search Phrase:  
            <br></br>
            <input type="text" name="word" required/>
          </label>
          <br></br>
          <button type="submit">
            Submit
          </button>
        </form>
      </div>
    </>
  )
}

export default App
