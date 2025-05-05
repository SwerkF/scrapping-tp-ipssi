import { useQuery } from '@tanstack/react-query';
import { articleService } from '../articleService';

interface GetArticlesData {
    search: string;
    page: number;
    limit: number;
    subCategory: string;
    category: string;
    startDate: string;
    endDate: string;
}
export const useGetArticles = (params: GetArticlesData) => {
    return useQuery({
        queryKey: [
            'articles',
            params.search,
            params.page,
            params.limit,
            params.subCategory,
            params.category,
            params.startDate,
            params.endDate,
        ],
        queryFn: async () => {
            let data = await articleService.getArticles({
                search: params.search,
                page: params.page,
                limit: params.limit,
                subCategory: params.subCategory,
                category: params.category,
                startDate: params.startDate,
                endDate: params.endDate,
            });
            return data;
        },
    });
};

export const useGetCategories = () => {
    return useQuery({
        queryKey: ['categories'],
        queryFn: async () => {
            let data = await articleService.getCategories();
            return data;
        },
    });
};
