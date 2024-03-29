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
								user: {
									id: string;
								};
								done: [boolean, boolean, boolean];
						  }[];
					id: string;
					file: string;
					fileUrl: string;
					video: string;
					quiz: null | string;
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

interface courseModes {
	all: 'all';
	ongoing: 'ongoing';
	done: 'done';
	initial: 'initial';
}

export type { GetUserTriosCourses, GetCourse, UpdateUserTrio, courseModes };
