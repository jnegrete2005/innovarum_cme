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
					usertrioSet:
						| null
						| {
								done: [boolean, boolean, boolean];
						  }[];
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

type UpdateUserTrio = {
	data: {
		updateUsertrio: {
			trio: {
				id: string;
				done: [boolean, boolean, boolean];
			};
		};
	};
};

export type { GetUserTriosCourses, GetCourse, UpdateUserTrio };
