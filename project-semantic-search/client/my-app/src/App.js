
import { useState } from "react";

function App() {
  const [query, setQuery] = useState(""); 
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState(null); 
  const [searchType, setSearchType] = useState("keyword");

  const handleSearch = async () => {
    if (!query) {
      setError("Search query cannot be empty.");
      setMovies([]);
      return;
    }

    setError(null);
    setMovies([]);
    console.log(`Searching for "${query}" using ${searchType} search`);

    try {
      // API endpoint based on search type
      const response = await fetch(
        searchType === "keyword"
          ? `/search?query=${encodeURIComponent(query)}`
          : `/semantic-search?query=${encodeURIComponent(query)}`
      );

      console.log("Response status:", response.status);

      if (response.status === 200) {
        const data = await response.json();
        console.log("Search results:", data);
        setMovies(data);
      } else {
        const errorData = await response.json();
        console.error("Server error:", errorData);
        setError(errorData.error || "An unknown error occurred.");
      }
    } catch (e) {
      console.error("Fetch error:", e);
      setError("Failed to fetch data. Please check the server.");
    }
  };

  return (
    <div className="App" style={{ textAlign: "center", marginTop: "20px" }}>
      <h1>Movie Search</h1>

      {/* Search type selection */}
      <div style={{ marginBottom: "20px" }}>
        <button
          onClick={() => {
            setSearchType("keyword");
            setMovies([]);
            setQuery("");
            setError(null);
          }}
          style={{
            backgroundColor: searchType === "keyword" ? "#4CAF50" : "#f0f0f0",
            color: searchType === "keyword" ? "white" : "black",
            margin: "5px",
            padding: "10px",
            border: "none",
            cursor: "pointer",
          }}
        >
          Keyword Search
        </button>
        <button
          onClick={() => {
            setSearchType("semantic");
            setMovies([]);
            setQuery("");
            setError(null);
          }}
          style={{
            backgroundColor: searchType === "semantic" ? "#4CAF50" : "#f0f0f0",
            color: searchType === "semantic" ? "white" : "black",
            margin: "5px",
            padding: "10px",
            border: "none",
            cursor: "pointer",
          }}
        >
          Semantic Search
        </button>
      </div>

      {/* Search input */}
      <div>
        <h2>{searchType === "keyword" ? "Keyword Search" : "Semantic Search"}</h2>
        <input
          type="text"
          placeholder={`Enter a movie title for ${searchType} search`}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{
            padding: "10px",
            marginRight: "10px",
            width: "300px",
            border: "1px solid #ccc",
            borderRadius: "5px",
          }}
        />
        <button
          onClick={handleSearch}
          style={{
            padding: "10px",
            backgroundColor: "#008CBA",
            color: "white",
            border: "none",
            cursor: "pointer",
            borderRadius: "5px",
          }}
        >
          Search
        </button>
      </div>

      {/* Error handling */}
      {error && <p style={{ color: "red", marginTop: "20px" }}>{error}</p>}

      {/* Display results */}
      <div style={{ marginTop: "20px" }}>
        {movies.length > 0 ? (
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            {movies.map((movie, index) => (
              <div
                key={index}
                style={{
                  margin: "10px 0",
                  padding: "10px 20px",
                  backgroundColor: "#f9f9f9",
                  borderRadius: "5px",
                  boxShadow: "0px 0px 5px rgba(0,0,0,0.1)",
                  width: "50%",
                  textAlign: "center",
                }}
              >
                {movie.title}
              </div>
            ))}
          </div>
        ) : (
          <p style={{ textAlign: "center", marginTop: "20px" }}>
            No results found. Try a different search.
          </p>
        )}
      </div>

    </div>
  );
}

export default App;
