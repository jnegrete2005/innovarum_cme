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

export type { GetUserTriosCourses };
