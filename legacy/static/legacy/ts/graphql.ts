type GetUserTriosCourses = {
	data: {
		user?: {
			usertrioSet: {
				trio: {
					module: {
						course: {
							id: string;
						};
					};
				};
				done: [boolean, boolean, boolean];
			}[];
		};
		courses: {
			id: number;
			name: string;
			img: string;
			modules?: {
				trios?: {
					id: string;
				}[];
			}[];
		}[];
	};
};

type GetCourse = {
	data: {
		course: {
			id: string;
			name: string;
			modules?: {
				trios?: {
					id: string;
					file: string;
					video: string;
					quiz: null | {
						id: string;
					};
				}[];
			}[];
		};
	};
};

export type { GetUserTriosCourses, GetCourse };
