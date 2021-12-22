type GetUserFileCourses = {
	data: {
		user?: {
			userfileSet: {
				file: {
					module: {
						course: {
							id: string;
						};
					};
				};
				done: boolean;
			}[];
		};
		trainingCourses: {
			id: number;
			name: string;
			img: string;
			modules?: {
				files?: {
					id: string;
				}[];
			}[];
		}[];
	};
};

type GetCourse = {
	data: {
		trainingCourse: {
			id: string;
			name: string;
			modules?: {
				name: string;
				files?: {
					userfileSet:
						| null
						| {
								user: {
									id: string;
								};
								done: boolean;
						  }[];
					id: string;
					name: string;
					url: string;
					fileType: 'A_1' | 'A_2';
				}[];
			}[];
		};
	};
};

type UpdateUserFile = {
	data: {
		updateUserfile: {
			file: {
				id: string;
				done: boolean;
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

export type { GetUserFileCourses, GetCourse, UpdateUserFile, courseModes };
