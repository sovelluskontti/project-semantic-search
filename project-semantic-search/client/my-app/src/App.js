
// import { useState } from "react";

// function App() {
//   const [query, setQuery] = useState(""); 
//   const [movies, setMovies] = useState([]);
//   const [error, setError] = useState(null); 
//   const [searchType, setSearchType] = useState("keyword");

//   const handleSearch = async () => {
//     if (!query) {
//       setError("Search query cannot be empty.");
//       setMovies([]);
//       return;
//     }

//     setError(null);
//     setMovies([]);
//     console.log(`Searching for "${query}" using ${searchType} search`);

//     try {
//       // API endpoint based on search type
//       const response = await fetch(
//         searchType === "keyword"
//           ? `/search?query=${encodeURIComponent(query)}`
//           : `/semantic-search?query=${encodeURIComponent(query)}`
//       );

//       console.log("Response status:", response.status);

//       if (response.status === 200) {
//         const data = await response.json();
//         console.log("Search results:", data);
//         setMovies(data);
//       } else {
//         const errorData = await response.json();
//         console.error("Server error:", errorData);
//         setError(errorData.error || "An unknown error occurred.");
//       }
//     } catch (e) {
//       console.error("Fetch error:", e);
//       setError("Failed to fetch data. Please check the server.");
//     }
//   };

//   return (
//     <div className="App" style={{ textAlign: "center", marginTop: "20px" }}>
//       <h1>Movie Search</h1>

//       {/* Search type selection */}
//       <div style={{ marginBottom: "20px" }}>
//         <button
//           onClick={() => {
//             setSearchType("keyword");
//             setMovies([]);
//             setQuery("");
//             setError(null);
//           }}
//           style={{
//             backgroundColor: searchType === "keyword" ? "#4CAF50" : "#f0f0f0",
//             color: searchType === "keyword" ? "white" : "black",
//             margin: "5px",
//             padding: "10px",
//             border: "none",
//             cursor: "pointer",
//           }}
//         >
//           Keyword Search
//         </button>
//         <button
//           onClick={() => {
//             setSearchType("semantic");
//             setMovies([]);
//             setQuery("");
//             setError(null);
//           }}
//           style={{
//             backgroundColor: searchType === "semantic" ? "#4CAF50" : "#f0f0f0",
//             color: searchType === "semantic" ? "white" : "black",
//             margin: "5px",
//             padding: "10px",
//             border: "none",
//             cursor: "pointer",
//           }}
//         >
//           Semantic Search
//         </button>
//       </div>

//       {/* Search input */}
//       <div>
//         <h2>{searchType === "keyword" ? "Keyword Search" : "Semantic Search"}</h2>
//         <input
//           type="text"
//           placeholder={`Enter a movie title for ${searchType} search`}
//           value={query}
//           onChange={(e) => setQuery(e.target.value)}
//           style={{
//             padding: "10px",
//             marginRight: "10px",
//             width: "300px",
//             border: "1px solid #ccc",
//             borderRadius: "5px",
//           }}
//         />
//         <button
//           onClick={handleSearch}
//           style={{
//             padding: "10px",
//             backgroundColor: "#008CBA",
//             color: "white",
//             border: "none",
//             cursor: "pointer",
//             borderRadius: "5px",
//           }}
//         >
//           Search
//         </button>
//       </div>

//       {/* Error handling */}
//       {error && <p style={{ color: "red", marginTop: "20px" }}>{error}</p>}

//       {/* Display results */}
//       <div style={{ marginTop: "20px" }}>
//         {movies.length > 0 ? (
//           <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
//             {movies.map((movie, index) => (
//               <div
//                 key={index}
//                 style={{
//                   margin: "10px 0",
//                   padding: "10px 20px",
//                   backgroundColor: "#f9f9f9",
//                   borderRadius: "5px",
//                   boxShadow: "0px 0px 5px rgba(0,0,0,0.1)",
//                   width: "50%",
//                   textAlign: "center",
//                 }}
//               >
//                 {movie.title}
//               </div>
//             ))}
//           </div>
//         ) : (
//           <p style={{ textAlign: "center", marginTop: "20px" }}>
//             No results found. Try a different search.
//           </p>
//         )}
//       </div>

//     </div>
//   );
// }

// export default App;



import { useState, useEffect } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [movies, setMovies] = useState(null);
  const [error, setError] = useState(null);
  const [searchType, setSearchType] = useState("keyword");

  const [category, setCategory] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [productSearch, setProductSearch] = useState(""); // product name search box

  const handleSearch = async () => {
    setError(null);
    setMovies(null);
    console.log(`Searching using ${searchType} search`);

    try {
      let response;
      if (searchType === "keyword" || searchType === "semantic") {
        if (!query) {
          setError("Search query cannot be empty.");
          return;
        }
        response = await fetch(
          searchType === "keyword"
            ? `/search?query=${encodeURIComponent(query)}`
            : `/semantic-search?query=${encodeURIComponent(query)}`
        );
      } else if (searchType === "faceted") {
        const params = new URLSearchParams();
        if (category) params.append("category", category);
        if (minPrice) params.append("min_price", minPrice);
        if (maxPrice) params.append("max_price", maxPrice);
        if (productSearch) params.append("name", productSearch);
        response = await fetch(`/faceted-search?${params.toString()}`);
      }

      console.log("Response status:", response.status);

      if (response.ok) {
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

  useEffect(() => {
    if (searchType === "faceted") {
      handleSearch();
    }
  }, [searchType]);

  const resetState = (type) => {
    setSearchType(type);
    setMovies(null);
    setError(null);
    setQuery("");
    setCategory("");
    setMinPrice("");
    setMaxPrice("");
    setProductSearch("");
  };

  return (
    <div className="App" style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      <h1 style={{ textAlign: "center", marginTop: "20px" }}>Product & Movie Search</h1>

      {/* Search Type Buttons */}
      <div style={{ textAlign: "center", marginBottom: "20px" }}>
        {["keyword", "semantic", "faceted"].map((type) => (
          <button
            key={type}
            onClick={() => resetState(type)}
            style={{
              backgroundColor: searchType === type ? "#4CAF50" : "#f0f0f0",
              color: searchType === type ? "white" : "black",
              margin: "5px",
              padding: "10px",
              border: "none",
              cursor: "pointer",
            }}
          >
            {type.charAt(0).toUpperCase() + type.slice(1)} Search
          </button>
        ))}
      </div>

      {/* Main content area */}
      <div style={{ display: "flex", flex: 1 }}>
        {/* Sidebar Filters */}
        {searchType === "faceted" && (
          <div
            style={{
              width: "25%",
              backgroundColor: "#f8f8f8",
              padding: "20px",
              boxShadow: "2px 0 5px rgba(0,0,0,0.1)",
            }}
          >
            <h2 style={{ textAlign: "center" }}>Faceted Filters</h2>

            {/* Category */}
            <input
              type="text"
              placeholder="Category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              style={{
                padding: "10px",
                marginBottom: "10px",
                width: "100%",
                border: "1px solid #ccc",
                borderRadius: "5px",
              }}
            />

            {/* Price */}
            <input
              type="number"
              placeholder="Min Price"
              value={minPrice}
              onChange={(e) => setMinPrice(e.target.value)}
              style={{
                padding: "10px",
                marginBottom: "10px",
                width: "100%",
                border: "1px solid #ccc",
                borderRadius: "5px",
              }}
            />
            <input
              type="number"
              placeholder="Max Price"
              value={maxPrice}
              onChange={(e) => setMaxPrice(e.target.value)}
              style={{
                padding: "10px",
                marginBottom: "10px",
                width: "100%",
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
                width: "100%",
                cursor: "pointer",
                borderRadius: "5px",
              }}
            >
              Apply Filters
            </button>
          </div>
        )}

        {/* Main Product/Movie Display */}
        <div
          style={{
            flex: 1,
            padding: "20px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          {/* Product Name Search Bar for Faceted Search */}
          {searchType === "faceted" && (
            <div style={{ marginBottom: "20px", display: "flex", alignItems: "center" }}>
              <input
                type="text"
                placeholder="Search product name"
                value={productSearch}
                onChange={(e) => setProductSearch(e.target.value)}
                style={{
                  padding: "10px",
                  marginRight: "10px",
                  width: "400px",
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
          )}

          {/* Keyword / Semantic search input */}
          {(searchType === "keyword" || searchType === "semantic") && (
            <div style={{ marginBottom: "20px" }}>
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
          )}

          {/* Error */}
          {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}

          {/* Results */}
          <div style={{ width: "80%", marginTop: "20px" }}>
            {movies === null ? null : movies.length > 0 ? (
              movies.map((item, index) => (
                <div
                  key={index}
                  style={{
                    margin: "10px 0",
                    padding: "10px 20px",
                    backgroundColor: "#f9f9f9",
                    borderRadius: "5px",
                    boxShadow: "0px 0px 5px rgba(0,0,0,0.1)",
                    textAlign: "center",
                  }}
                >
                  {searchType === "faceted"
                    ? `${item.name} | ${item.category} | ${item.manufacturer} | $${item.price} | ${item.description}`
                    : item.title}
                </div>
              ))
            ) : (
              <p style={{ textAlign: "center", marginTop: "20px" }}>
                No results found. Try a different search.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
