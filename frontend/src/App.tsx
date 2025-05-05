import { useState } from 'react';
import './App.css';
import { useGetArticles, useGetCategories } from './api/queries/articleQueries';

function App() {
    const [search, setSearch] = useState('');
    const [page, setPage] = useState(1);
    const [limit, setLimit] = useState(10);
    const [subCategory, setSubCategory] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('');
    const [searchInput, setSearchInput] = useState('');
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');

    const { data, isLoading, error } = useGetArticles({
        search,
        page,
        limit,
        subCategory,
        category: selectedCategory,
        startDate,
        endDate,
    });

    const { data: categories } = useGetCategories();

    const handleSearchSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setSearch(searchInput);
        setPage(1);
    };

    return (
        <div className="mx-auto max-w-7xl bg-gray-100 min-h-screen p-4">
            <header className="py-6">
                <h1 className="text-3xl font-bold text-center text-blue-800">Blog du Modérateur</h1>
            </header>

            <div className="mb-6">
                <form onSubmit={handleSearchSubmit} className="flex gap-2">
                    <input
                        type="text"
                        value={searchInput}
                        onChange={(e) => setSearchInput(e.target.value)}
                        placeholder="Rechercher des articles..."
                        className="flex-grow p-2 border rounded-md"
                    />
                    <button
                        type="submit"
                        className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                    >
                        Rechercher
                    </button>
                </form>
            </div>

            <div className="mb-6">
                <div className="flex flex-row gap-2">
                    <div className="flex flex-col gap-2">
                        <label
                            htmlFor="startDate"
                            className="block text-sm font-medium text-gray-700 mb-1"
                        >
                            Date de début
                        </label>
                        <input
                            type="date"
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                            className="p-2 border rounded-md"
                        />
                        <button
                            onClick={() => setStartDate('')}
                            className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700"
                        >
                            Effacer
                        </button>
                    </div>
                    <div className="flex flex-col gap-2">
                        <label
                            htmlFor="endDate"
                            className="block text-sm font-medium text-gray-700 mb-1"
                        >
                            Date de fin
                        </label>
                        <input
                            type="date"
                            value={endDate}
                            onChange={(e) => setEndDate(e.target.value)}
                            className="p-2 border rounded-md"
                        />
                        <button
                            onClick={() => setEndDate('')}
                            className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700"
                        >
                            Effacer
                        </button>
                    </div>
                </div>
                <div className="flex flex-col gap-2">
                    {categories &&
                        categories?.categories?.map((category: any, index: number) => {
                            return (
                                <div className="flex flex-col gap-2">
                                    <p key={index} className="text-lg font-semibold">
                                        {category.name.toUpperCase()}
                                    </p>
                                    <div className="flex flex-row flex-wrap gap-2">
                                        {category.sub_categories
                                            .sort((a: any, b: any) => a.name.localeCompare(b.name))
                                            .map((sub_category: any, index: number) => {
                                                return (
                                                    <button
                                                        key={index}
                                                        onClick={() => {
                                                            setSubCategory(sub_category.name);
                                                            setSelectedCategory(category.name);
                                                        }}
                                                        className={
                                                            sub_category.name === subCategory &&
                                                            category.name === selectedCategory
                                                                ? 'bg-blue-600 text-white px-2 py-1 text-sm rounded-md hover:bg-blue-700'
                                                                : 'bg-gray-200 text-gray-700 px-2 py-1 text-sm rounded-md hover:bg-gray-300'
                                                        }
                                                    >
                                                        {sub_category.name}
                                                    </button>
                                                );
                                            })}
                                    </div>
                                </div>
                            );
                        })}
                    <button
                        onClick={() => {
                            setSubCategory('');
                            setSelectedCategory('');
                        }}
                        className={
                            subCategory === '' && selectedCategory === ''
                                ? 'bg-blue-600 text-white px-2 py-1 text-sm rounded-md hover:bg-blue-700'
                                : 'bg-gray-200 text-gray-700 px-2 py-1 text-sm rounded-md hover:bg-gray-300'
                        }
                    >
                        Toutes les catégories
                    </button>
                </div>
            </div>

            <div className="mb-6">
                <label htmlFor="limit" className="block text-sm font-medium text-gray-700 mb-1">
                    Articles par page:
                </label>
                <select
                    id="limit"
                    value={limit}
                    onChange={(e) => {
                        setLimit(Number(e.target.value));
                        setPage(1);
                    }}
                    className="p-2 border rounded-md"
                >
                    <option value="5">5</option>
                    <option value="10">10</option>
                    <option value="20">20</option>
                    <option value="50">50</option>
                </select>
            </div>

            {isLoading && <p className="text-center">Chargement des articles...</p>}
            {error && (
                <p className="text-center text-red-500">
                    Une erreur est survenue lors du chargement des articles
                </p>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
                {data?.articles.map((article: any) => (
                    <div
                        key={article._id}
                        className="bg-white rounded-lg shadow-md overflow-hidden"
                    >
                        <img
                            src={article.thumbnail}
                            alt={article.title}
                            className="w-full h-48 object-cover"
                        />
                        <div className="p-4">
                            <div className="flex flex-wrap gap-2 mb-3"></div>
                            <h2 className="text-xl font-semibold mb-2">{article.title}</h2>
                            <p className="text-gray-600 text-sm mb-3">{article.resume}</p>
                            <div className="flex justify-between items-center text-xs text-gray-500">
                                <span>{article.author}</span>
                                <span>{new Date(article.posted_on).toLocaleDateString('FR')}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {data && (
                <div className="mt-8 flex justify-center">
                    <div className="flex items-center gap-2">
                        <button
                            onClick={() => setPage((p) => Math.max(1, p - 1))}
                            disabled={page === 1}
                            className={`px-4 py-2 rounded-md ${
                                page === 1
                                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                                    : 'bg-blue-600 text-white hover:bg-blue-700'
                            }`}
                        >
                            Précédent
                        </button>
                        <div className="flex items-center gap-2">
                            {(() => {
                                let pageButtons = [];
                                let startPage = Math.max(1, page - 1);
                                let endPage = Math.min(startPage + 2, data.max_page);

                                // Ajuster startPage si on est proche de la fin
                                if (endPage - startPage < 2) {
                                    startPage = Math.max(1, endPage - 2);
                                }

                                for (let i = startPage; i <= endPage; i++) {
                                    pageButtons.push(
                                        <button
                                            key={i}
                                            onClick={() => setPage(i)}
                                            className={`w-8 h-8 flex items-center justify-center rounded-md ${
                                                page === i
                                                    ? 'bg-blue-600 text-white'
                                                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                            }`}
                                        >
                                            {i}
                                        </button>
                                    );
                                }
                                return pageButtons;
                            })()}
                            {page + 2 < data.max_page && (
                                <>
                                    <span className="text-gray-700">...</span>
                                    <button
                                        onClick={() => setPage(data.max_page)}
                                        className={`w-8 h-8 flex items-center justify-center rounded-md ${
                                            page === data.max_page
                                                ? 'bg-blue-600 text-white'
                                                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                        }`}
                                    >
                                        {data.max_page}
                                    </button>
                                </>
                            )}
                        </div>
                        <button
                            onClick={() => setPage((p) => Math.min(data.max_page, p + 1))}
                            disabled={page === data.max_page}
                            className={`px-4 py-2 rounded-md ${
                                page === data.max_page
                                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                                    : 'bg-blue-600 text-white hover:bg-blue-700'
                            }`}
                        >
                            Suivant
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;
