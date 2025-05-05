import { api } from './interceptor';

interface GetArticlesData {
    search: string;
    page: number;
    limit: number;
    subCategory: string;
    category: string;
    startDate: string;
    endDate: string;
}

class ArticleService {
    private readonly apiUrl = 'api/articles';
    private readonly categoriesUrl = 'api/categories';

    public async getArticles(data: GetArticlesData) {
        let searchParams = new URLSearchParams();
        if (data.search) searchParams.set('search', data.search);
        if (data.page) searchParams.set('page', data.page.toString());
        if (data.limit) searchParams.set('limit', data.limit.toString());
        if (data.subCategory) searchParams.set('subCategory', data.subCategory);
        if (data.category) searchParams.set('category', data.category);
        if (data.startDate) searchParams.set('startDate', data.startDate);
        if (data.endDate) searchParams.set('endDate', data.endDate);
        return await api.fetchRequest(
            `${this.apiUrl}?${searchParams.toString()}`,
            'GET',
            null,
            true
        );
    }

    public async getCategories() {
        return await api.fetchRequest(this.categoriesUrl, 'GET', null, true);
    }
}

export const articleService = new ArticleService();
