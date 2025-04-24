// import React, { useState, useEffect } from 'react';
// import { Book, Search, ArrowRight } from 'lucide-react';
// import axios from 'axios';

// const BookRecommender = () => {
//   const [books, setBooks] = useState([]);
//   const [selectedBook, setSelectedBook] = useState('');
//   const [recommendations, setRecommendations] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   // Fetch all available books on component mount
//   useEffect(() => {
//     const fetchBooks = async () => {
//       try {
//         setLoading(true);
//         const response = await axios.get('/books');
//         setBooks(response.data.books || []);
//         setLoading(false);
//       } catch (err) {
//         setError('Failed to load books. Please try again later.');
//         setLoading(false);
//       }
//     };

//     fetchBooks();
//   }, []);

//   // Handle book selection and fetch recommendations
//   const handleGetRecommendations = async () => {
//     if (!selectedBook) return;
    
//     try {
//       setLoading(true);
//       setRecommendations([]);
      
//       const response = await axios.get(`/api/books/recommend/${encodeURIComponent(selectedBook)}`);
//       setRecommendations(response.data.recommended_books || []);
//       setLoading(false);
//     } catch (err) {
//       setError('Failed to get recommendations. Please try again later.');
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="w-full max-w-7xl mx-auto px-4 py-12">
//       {/* Header Section */}
//       <section className="text-center mb-12">
//         <div className="flex justify-center mb-4">
//           <Book className="h-16 w-16 text-purple-600" />
//         </div>
//         <h1 className="text-4xl font-bold text-gray-900 mb-4">Book Recommendations</h1>
//         <p className="text-lg text-gray-600 max-w-xl mx-auto">
//           Discover books that inspire, comfort, and support your mental well-being journey.
//         </p>
//       </section>

//       {/* Selection Section */}
//       <section className="bg-purple-50 rounded-2xl p-8 shadow-lg mb-12">
//         <h2 className="text-2xl font-semibold text-gray-800 mb-6">Find Your Next Read</h2>
        
//         <div className="max-w-xl mx-auto">
//           <div className="mb-6">
//             <label htmlFor="book-select" className="block text-sm font-medium text-gray-700 mb-2">
//               Select a book you enjoyed
//             </label>
//             <div className="flex gap-4">
//               <select
//                 id="book-select"
//                 value={selectedBook}
//                 onChange={(e) => setSelectedBook(e.target.value)}
//                 className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
//               >
//                 <option value="">Select a book...</option>
//                 {books.map((book) => (
//                   <option key={book.id} value={book.title}>
//                     {book.title}
//                   </option>
//                 ))}
//               </select>
//               <button
//                 onClick={handleGetRecommendations}
//                 disabled={!selectedBook || loading}
//                 className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-lg shadow-md transition-colors flex items-center"
//               >
//                 {loading ? 'Loading...' : (
//                   <>
//                     Get Recommendations
//                     <ArrowRight className="ml-2 h-5 w-5" />
//                   </>
//                 )}
//               </button>
//             </div>
//           </div>
//         </div>
//       </section>

//       {/* Error Message */}
//       {error && (
//         <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8">
//           <div className="flex">
//             <div className="flex-shrink-0">
//               <svg className="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
//                 <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
//               </svg>
//             </div>
//             <div className="ml-3">
//               <p className="text-sm text-red-700">{error}</p>
//             </div>
//           </div>
//         </div>
//       )}

//       {/* Results Section */}
//       {recommendations.length > 0 && (
//         <section className="mb-12">
//           <h2 className="text-2xl font-semibold text-gray-800 mb-8 text-center">
//             Books You Might Enjoy
//           </h2>
          
//           <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
//             {recommendations.map((book, index) => (
//               <div 
//                 key={index} 
//                 className="bg-white rounded-lg overflow-hidden shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
//               >
//                 <div className="h-64 overflow-hidden">
//                   <img 
//                     src={book.image_url} 
//                     alt={book.title} 
//                     className="w-full h-full object-cover"
//                     onError={(e) => {
//                       e.target.src = "https://via.placeholder.com/300x450?text=Book+Cover";
//                     }}
//                   />
//                 </div>
//                 <div className="p-4">
//                   <h3 className="font-medium text-gray-900 text-lg line-clamp-2 h-14">
//                     {book.title}
//                   </h3>
//                   <button className="mt-4 text-purple-600 hover:text-purple-800 font-medium flex items-center text-sm">
//                     View Details
//                     <ArrowRight className="ml-1 h-4 w-4" />
//                   </button>
//                 </div>
//               </div>
//             ))}
//           </div>
//         </section>
//       )}

//       {/* No Results Message */}
//       {selectedBook && !loading && recommendations.length === 0 && !error && (
//         <div className="text-center py-12">
//           <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
//           <h3 className="text-xl font-medium text-gray-600">Select a book to get recommendations</h3>
//         </div>
//       )}

//       {/* Info Section */}
//       <section className="bg-indigo-50 rounded-xl p-8 mt-8">
//         <div className="max-w-3xl mx-auto">
//           <h2 className="text-2xl font-semibold text-indigo-900 mb-4">How It Works</h2>
//           <p className="text-gray-700 mb-6">
//             Our book recommendation system uses advanced similarity algorithms to suggest books based on your selection. 
//             These recommendations are tailored to provide reading experiences that complement your mental wellness journey.
//           </p>
//           <div className="grid md:grid-cols-3 gap-6">
//             <div className="bg-white p-5 rounded-lg shadow">
//               <div className="text-indigo-600 font-bold mb-2">Step 1</div>
//               <p className="text-gray-600">Select a book you've enjoyed reading</p>
//             </div>
//             <div className="bg-white p-5 rounded-lg shadow">
//               <div className="text-indigo-600 font-bold mb-2">Step 2</div>
//               <p className="text-gray-600">Click the "Get Recommendations" button</p>
//             </div>
//             <div className="bg-white p-5 rounded-lg shadow">
//               <div className="text-indigo-600 font-bold mb-2">Step 3</div>
//               <p className="text-gray-600">Discover new books tailored to your taste</p>
//             </div>
//           </div>
//         </div>
//       </section>
//     </div>
//   );
// };

// export default BookRecommender;

// import React, { useState, useEffect } from 'react';
// import { Book, Search, ArrowRight } from 'lucide-react';
// import axios from 'axios';

// const BookRecommender = () => {
//   const [books, setBooks] = useState([]);
//   const [selectedBook, setSelectedBook] = useState('');
//   const [recommendations, setRecommendations] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [loadingBooks, setLoadingBooks] = useState(true);
//   const [error, setError] = useState(null);

//   // Fetch all available books on component mount
//   useEffect(() => {
//     const fetchBooks = async () => {
//       try {
//         setLoadingBooks(true);
//         // Make sure the API endpoint matches your backend
//         const response = await axios.get('/books');
        
//         console.log("Books API response:", response.data); // Debugging
        
//         // Handle different response structures
//         if (response.data && response.data.books) {
//           setBooks(response.data.books);
//         } else if (Array.isArray(response.data)) {
//           setBooks(response.data);
//         } else {
//           console.error("Unexpected data format:", response.data);
//           setError("Received unexpected data format from server");
//         }
        
//         setLoadingBooks(false);
//       } catch (err) {
//         console.error("Error fetching books:", err);
//         setError('Failed to load books. Please try again later.');
//         setLoadingBooks(false);
//       }
//     };

//     fetchBooks();
//   }, []);

//   // Handle book selection and fetch recommendations
//   const handleGetRecommendations = async () => {
//     if (!selectedBook) return;
    
//     try {
//       setLoading(true);
//       setRecommendations([]);
      
//       const response = await axios.get(`/api/books/recommend/${encodeURIComponent(selectedBook)}`);
//       console.log("Recommendations response:", response.data); // Debugging
      
//       if (response.data && response.data.recommended_books) {
//         setRecommendations(response.data.recommended_books);
//       } else if (Array.isArray(response.data)) {
//         setRecommendations(response.data);
//       } else {
//         console.error("Unexpected recommendations format:", response.data);
//         setError("Received unexpected data format from server");
//       }
      
//       setLoading(false);
//     } catch (err) {
//       console.error("Error getting recommendations:", err);
//       setError('Failed to get recommendations. Please try again later.');
//       setLoading(false);
//     }
//   };

//   // For debugging - show what data we have
//   console.log("Books array:", books);
//   console.log("Books length:", books.length);

//   return (
//     <div className="w-full max-w-7xl mx-auto px-4 py-12">
//       {/* Header Section */}
//       <section className="text-center mb-12">
//         <div className="flex justify-center mb-4">
//           <Book className="h-16 w-16 text-purple-600" />
//         </div>
//         <h1 className="text-4xl font-bold text-gray-900 mb-4">Book Recommendations</h1>
//         <p className="text-lg text-gray-600 max-w-xl mx-auto">
//           Discover books that inspire, comfort, and support your mental well-being journey.
//         </p>
//       </section>

//       {/* Selection Section */}
//       <section className="bg-purple-50 rounded-2xl p-8 shadow-lg mb-12">
//         <h2 className="text-2xl font-semibold text-gray-800 mb-6">Find Your Next Read</h2>
        
//         <div className="max-w-xl mx-auto">
//           <div className="mb-6">
//             <label htmlFor="book-select" className="block text-sm font-medium text-gray-700 mb-2">
//               Select a book you enjoyed
//             </label>
//             <div className="flex flex-col sm:flex-row gap-4">
//               {loadingBooks ? (
//                 <div className="flex-1 p-3 border border-gray-300 rounded-lg bg-gray-50">
//                   Loading books...
//                 </div>
//               ) : books.length > 0 ? (
//                 <select
//                   id="book-select"
//                   value={selectedBook}
//                   onChange={(e) => setSelectedBook(e.target.value)}
//                   className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
//                 >
//                   <option value="">Select a book...</option>
//                   {books.map((book) => (
//                     <option key={book.id || `book-${Math.random()}`} value={book.title || book}>
//                       {book.title || book}
//                     </option>
//                   ))}
//                 </select>
//               ) : (
//                 <div className="flex-1 p-3 border border-gray-300 rounded-lg bg-gray-50 text-red-500">
//                   No books available. {error ? error : "Please try refreshing the page."}
//                 </div>
//               )}
//               <button
//                 onClick={handleGetRecommendations}
//                 disabled={!selectedBook || loading || loadingBooks}
//                 className={`px-6 py-3 font-medium rounded-lg shadow-md transition-colors flex items-center justify-center ${
//                   !selectedBook || loading || loadingBooks 
//                   ? "bg-gray-400 text-white cursor-not-allowed" 
//                   : "bg-purple-600 hover:bg-purple-700 text-white"
//                 }`}
//               >
//                 {loading ? 'Loading...' : (
//                   <>
//                     Get Recommendations
//                     <ArrowRight className="ml-2 h-5 w-5" />
//                   </>
//                 )}
//               </button>
//             </div>
            
//             {/* API Endpoint Debug Information */}
//             <div className="mt-4 text-sm text-gray-500">
//               <details>
//                 <summary className="cursor-pointer">Troubleshooting Info</summary>
//                 <div className="mt-2 p-4 bg-gray-100 rounded-lg overflow-auto">
//                   <p><strong>Books API Endpoint:</strong> /api/books/</p>
//                   <p><strong>Books Count:</strong> {books.length}</p>
//                   <p><strong>Loading State:</strong> {loadingBooks ? "Loading" : "Completed"}</p>
//                   <p><strong>Error:</strong> {error || "None"}</p>
//                   <p className="mt-2 text-xs">If books aren't loading, check your API endpoint and network console.</p>
//                 </div>
//               </details>
//             </div>
//           </div>
//         </div>
//       </section>

//       {/* Error Message */}
//       {error && (
//         <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8">
//           <div className="flex">
//             <div className="flex-shrink-0">
//               <svg className="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
//                 <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
//               </svg>
//             </div>
//             <div className="ml-3">
//               <p className="text-sm text-red-700">{error}</p>
//             </div>
//           </div>
//         </div>
//       )}

//       {/* Results Section */}
//       {recommendations.length > 0 && (
//         <section className="mb-12">
//           <h2 className="text-2xl font-semibold text-gray-800 mb-8 text-center">
//             Books You Might Enjoy
//           </h2>
          
//           <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
//             {recommendations.map((book, index) => (
//               <div 
//                 key={index} 
//                 className="bg-white rounded-lg overflow-hidden shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
//               >
//                 <div className="h-64 overflow-hidden">
//                   <img 
//                     src={book.image_url || "https://via.placeholder.com/300x450?text=Book+Cover"} 
//                     alt={book.title || "Book cover"} 
//                     className="w-full h-full object-cover"
//                     onError={(e) => {
//                       e.target.src = "https://via.placeholder.com/300x450?text=Book+Cover";
//                     }}
//                   />
//                 </div>
//                 <div className="p-4">
//                   <h3 className="font-medium text-gray-900 text-lg line-clamp-2 h-14">
//                     {book.title || "Unknown Title"}
//                   </h3>
//                   <button className="mt-4 text-purple-600 hover:text-purple-800 font-medium flex items-center text-sm">
//                     View Details
//                     <ArrowRight className="ml-1 h-4 w-4" />
//                   </button>
//                 </div>
//               </div>
//             ))}
//           </div>
//         </section>
//       )}

//       {/* Loading Recommendations */}
//       {loading && (
//         <div className="text-center py-12">
//           <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500 mx-auto mb-4"></div>
//           <h3 className="text-xl font-medium text-gray-600">Finding books for you...</h3>
//         </div>
//       )}

//       {/* No Results Message */}
//       {selectedBook && !loading && recommendations.length === 0 && !error && (
//         <div className="text-center py-12">
//           <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
//           <h3 className="text-xl font-medium text-gray-600">No recommendations found. Try another book.</h3>
//         </div>
//       )}

//       {/* Info Section */}
//       <section className="bg-indigo-50 rounded-xl p-8 mt-8">
//         <div className="max-w-3xl mx-auto">
//           <h2 className="text-2xl font-semibold text-indigo-900 mb-4">How It Works</h2>
//           <p className="text-gray-700 mb-6">
//             Our book recommendation system uses advanced similarity algorithms to suggest books based on your selection. 
//             These recommendations are tailored to provide reading experiences that complement your mental wellness journey.
//           </p>
//           <div className="grid md:grid-cols-3 gap-6">
//             <div className="bg-white p-5 rounded-lg shadow">
//               <div className="text-indigo-600 font-bold mb-2">Step 1</div>
//               <p className="text-gray-600">Select a book you've enjoyed reading</p>
//             </div>
//             <div className="bg-white p-5 rounded-lg shadow">
//               <div className="text-indigo-600 font-bold mb-2">Step 2</div>
//               <p className="text-gray-600">Click the "Get Recommendations" button</p>
//             </div>
//             <div className="bg-white p-5 rounded-lg shadow">
//               <div className="text-indigo-600 font-bold mb-2">Step 3</div>
//               <p className="text-gray-600">Discover new books tailored to your taste</p>
//             </div>
//           </div>
//         </div>
//       </section>
//     </div>
//   );
// };

// export default BookRecommender;


import React, { useState, useEffect } from 'react';
import { Book, Search, ArrowRight } from 'lucide-react';
import axios from 'axios';

// Mock data for development when API is not available
const MOCK_BOOKS = [
  { id: 1, title: "The Alchemist" },
  { id: 2, title: "Atomic Habits" },
  { id: 3, title: "Thinking, Fast and Slow" },
  { id: 4, title: "Man's Search for Meaning" },
  { id: 5, title: "Mindfulness in Plain English" },
  { id: 6, title: "The Power of Now" },
  { id: 7, title: "Feeling Good" },
  { id: 8, title: "The Body Keeps the Score" }
];

const MOCK_RECOMMENDATIONS = [
  { title: "The Four Agreements", image_url: "https://m.media-amazon.com/images/I/91rR9gMuOVL.jpg" },
  { title: "Daring Greatly", image_url: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeFawuG6tASf3518NjhM5sQyfnDIHnOOywcQ&s" },
  { title: "The Untethered Soul", image_url: "https://m.media-amazon.com/images/I/51jaiwUXqVL._SL500_.jpg" },
  { title: "The Happiness Trap", image_url: "https://m.media-amazon.com/images/I/71kCQXpBqlL._AC_UF1000,1000_QL80_.jpg" }
];

// Set this to true to use mock data, false to use API
const USE_MOCK_DATA = true;

const BookRecommender = () => {
  const [books, setBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingBooks, setLoadingBooks] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBooks = async () => {
      if (USE_MOCK_DATA) {
        // Use mock data instead of API call
        setBooks(MOCK_BOOKS);
        setLoadingBooks(false);
        return;
      }

      try {
        setLoadingBooks(true);
        // Note: Using a full URL here instead of a relative path
        const response = await axios.get('http://localhost:8000/api/books');
        
        console.log("Books API response:", response.data);
        
        // Handle different response structures
        if (response.data && response.data.books) {
          setBooks(response.data.books);
        } else if (Array.isArray(response.data)) {
          setBooks(response.data);
        } else {
          console.error("Unexpected data format:", response.data);
          setError("Received unexpected data format from server");
        }
        
        setLoadingBooks(false);
      } catch (err) {
        console.error("Error fetching books:", err);
        setError('Failed to load books. Please try again later.');
        setLoadingBooks(false);
      }
    };

    fetchBooks();
  }, []);

  const handleGetRecommendations = async () => {
    if (!selectedBook) return;
    
    try {
      setLoading(true);
      setRecommendations([]);
      
      if (USE_MOCK_DATA) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 800));
        setRecommendations(MOCK_RECOMMENDATIONS);
        setLoading(false);
        return;
      }
      
      const response = await axios.get(`http://localhost:8000/api/books/recommend/${encodeURIComponent(selectedBook)}`);
      console.log("Recommendations response:", response.data);
      
      if (response.data && response.data.recommended_books) {
        setRecommendations(response.data.recommended_books);
      } else if (Array.isArray(response.data)) {
        setRecommendations(response.data);
      } else {
        console.error("Unexpected recommendations format:", response.data);
        setError("Received unexpected data format from server");
      }
      
      setLoading(false);
    } catch (err) {
      console.error("Error getting recommendations:", err);
      setError('Failed to get recommendations. Please try again later.');
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto px-4 py-12">
      {/* Header Section */}
      <section className="text-center mb-12">
        <div className="flex justify-center mb-4">
          <Book className="h-16 w-16 text-purple-600" />
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Book Recommendations</h1>
        <p className="text-lg text-gray-600 max-w-xl mx-auto">
          Discover books that inspire, comfort, and support your mental well-being journey.
        </p>
      </section>

      {/* Selection Section */}
      <section className="bg-purple-50 rounded-2xl p-8 shadow-lg mb-12">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6">Find Your Next Read</h2>
        
        <div className="max-w-xl mx-auto">
          <div className="mb-6">
            <label htmlFor="book-select" className="block text-sm font-medium text-gray-700 mb-2">
              Select a book you enjoyed
            </label>
            <div className="flex flex-col sm:flex-row gap-4">
              {loadingBooks ? (
                <div className="flex-1 p-3 border border-gray-300 rounded-lg bg-gray-50">
                  Loading books...
                </div>
              ) : books.length > 0 ? (
                <select
                  id="book-select"
                  value={selectedBook}
                  onChange={(e) => setSelectedBook(e.target.value)}
                  className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                >
                  <option value="">Select a book...</option>
                  {books.map((book) => (
                    <option key={book.id || `book-${Math.random()}`} value={book.title || book}>
                      {book.title || book}
                    </option>
                  ))}
                </select>
              ) : (
                <div className="flex-1 p-3 border border-gray-300 rounded-lg bg-gray-50 text-red-500">
                  No books available. {error ? error : "Please try refreshing the page."}
                </div>
              )}
              <button
                onClick={handleGetRecommendations}
                disabled={!selectedBook || loading || loadingBooks}
                className={`px-6 py-3 font-medium rounded-lg shadow-md transition-colors flex items-center justify-center ${
                  !selectedBook || loading || loadingBooks 
                  ? "bg-gray-400 text-white cursor-not-allowed" 
                  : "bg-purple-600 hover:bg-purple-700 text-white"
                }`}
              >
                {loading ? 'Loading...' : (
                  <>
                    Get Recommendations
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </>
                )}
              </button>
            </div>
            
            {/* Development mode notice */}
            {USE_MOCK_DATA && (
              <div className="mt-4 text-sm p-2 bg-yellow-50 border border-yellow-200 rounded-md text-yellow-700">
                <strong>Development Mode:</strong> Using mock data instead of API calls.
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Results Section */}
      {recommendations.length > 0 && (
        <section className="mb-12">
          <h2 className="text-2xl font-semibold text-gray-800 mb-8 text-center">
            Books You Might Enjoy
          </h2>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {recommendations.map((book, index) => (
              <div 
                key={index} 
                className="bg-white rounded-lg overflow-hidden shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
              >
                <div className="h-64 overflow-hidden">
                  <img 
                    src={book.image_url || "https://5.imimg.com/data5/IU/SQ/GD/SELLER-43618059/book-cover-page-design-1000x1000.jpg"} 
                    alt={book.title || "Book cover"} 
                    className="w-full h-full"
                    onError={(e) => {
                      e.target.src = "https://5.imimg.com/data5/IU/SQ/GD/SELLER-43618059/book-cover-page-design-1000x1000.jpg";
                    }}
                  />
                </div>
                <div className="p-4">
                  <h3 className="font-medium text-gray-900 text-lg line-clamp-2 h-14">
                    {book.title || "Unknown Title"}
                  </h3>
                  <button className="mt-4 text-purple-600 hover:text-purple-800 font-medium flex items-center text-sm">
                    View Details
                    <ArrowRight className="ml-1 h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Loading Recommendations */}
      {loading && (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500 mx-auto mb-4"></div>
          <h3 className="text-xl font-medium text-gray-600">Finding books for you...</h3>
        </div>
      )}

      {/* No Results Message */}
      {selectedBook && !loading && recommendations.length === 0 && !error && (
        <div className="text-center py-12">
          <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-medium text-gray-600">No recommendations found. Try another book.</h3>
        </div>
      )}

      {/* Info Section */}
      <section className="bg-indigo-50 rounded-xl p-8 mt-8">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-semibold text-indigo-900 mb-4">How It Works</h2>
          <p className="text-gray-700 mb-6">
            Our book recommendation system uses advanced similarity algorithms to suggest books based on your selection. 
            These recommendations are tailored to provide reading experiences that complement your mental wellness journey.
          </p>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white p-5 rounded-lg shadow">
              <div className="text-indigo-600 font-bold mb-2">Step 1</div>
              <p className="text-gray-600">Select a book you've enjoyed reading</p>
            </div>
            <div className="bg-white p-5 rounded-lg shadow">
              <div className="text-indigo-600 font-bold mb-2">Step 2</div>
              <p className="text-gray-600">Click the "Get Recommendations" button</p>
            </div>
            <div className="bg-white p-5 rounded-lg shadow">
              <div className="text-indigo-600 font-bold mb-2">Step 3</div>
              <p className="text-gray-600">Discover new books tailored to your taste</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default BookRecommender;