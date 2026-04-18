import { useState } from "react";

function App() {
  const [color, setColor] = useState("");
  const [fabric, setFabric] = useState("");
  const [outfit, setOutfit] = useState("");
  const [notes, setNotes] = useState("");
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateImage = async () => {
    setLoading(true);
    setImage(null);

    const res = await fetch("http://127.0.0.1:5000/generate-image", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ color, fabric, outfit, notes })
    });

    const data = await res.json();
    setLoading(false);

    if(data.image){
      setImage(data.image);
    } else {
      alert("Error: " + data.error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100 flex items-center justify-center">

      <div className="bg-white p-8 rounded-xl shadow-lg w-[420px]">

        <h1 className="text-2xl font-bold text-center mb-6">
          AI Fashion Image Generator
        </h1>

        <input
          placeholder="Color (e.g. Red)"
          className="border p-2 w-full mb-3"
          onChange={(e)=>setColor(e.target.value)}
        />

        <input
          placeholder="Fabric (e.g. Silk)"
          className="border p-2 w-full mb-3"
          onChange={(e)=>setFabric(e.target.value)}
        />

        <input
          placeholder="Outfit (e.g. Saree)"
          className="border p-2 w-full mb-3"
          onChange={(e)=>setOutfit(e.target.value)}
        />

        <input
          placeholder="Extra Notes"
          className="border p-2 w-full mb-4"
          onChange={(e)=>setNotes(e.target.value)}
        />

        <button
          onClick={generateImage}
          className="bg-purple-600 text-white py-2 rounded w-full"
        >
          Generate Image
        </button>

        {loading && (
          <p className="text-center mt-4">Generating image...</p>
        )}

        {image && (
          <img
            src={image}
            alt="Generated Fashion"
            className="mt-6 rounded-lg shadow"
          />
        )}

      </div>
    </div>
  );
}

export default App;
