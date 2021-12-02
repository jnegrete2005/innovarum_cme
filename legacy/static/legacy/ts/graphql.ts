type CoursesQuery = {
	data: {
		courses: [
			{
				id: number;
				name: string;
				img: string;
			}
		];
	};
};

export type { CoursesQuery };
