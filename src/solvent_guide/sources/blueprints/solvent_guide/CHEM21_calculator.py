def get_health_code_dict():
    health_code_dict = {
        2: ['H302', 'H304', 'H312', 'H315', 'H317', 'H319', 'H332', 'H335', 'H336', 'H371', 'H373', 'EUH070', 'EUH066'],
        4: ['H334', 'H318'],
        6: ['H301', 'H311', 'H331', 'H341', 'H351', 'H361', 'H370', 'H372'],
        7: ['H314'],
        9: ['H300', 'H310', 'H330', 'H350', 'H360']
        }
    return health_code_dict


def get_env_code_dict():
    env_code_dict = {5: ['H412', 'H413'],
                     7: ['H400', 'H410', 'H411'],
                     10: ['H420']
                     }
    return env_code_dict


class CHEM21Calculator:

    def __init__(self, flash_point, ignition_temp, hazard_codes, boiling_point, peroxability=False, resistivity=False, reach=False):
        self.flash_point = flash_point
        self.ignition_temp = ignition_temp
        self.hazard_codes = hazard_codes
        self.boiling_point = boiling_point
        self.peroxability = peroxability
        self.resistivity = resistivity
        self.reach = reach

    def get_flash_point_score(self):
        fp_score = 0
        if self.flash_point > 60:
            fp_score += 1
        elif 24 < self.flash_point < 60:
            fp_score += 3
        elif 0 < self.flash_point < 23:
            fp_score += 4
        elif -20 < self.flash_point < 0:
            fp_score += 5
        elif self.flash_point < -20:
            fp_score += 7
        return fp_score

    def get_ignition_temp_score(self):
        if self.ignition_temp > 200:
            return 0
        else:
            return 1

    def get_peroxability_score(self):

        if self.peroxability:
            return 1
        else:
            return 0

    def get_resistivity_score(self):

        if self.resistivity:
            return 1
        else:
            return 0

    def calculate_safety_score(self):
        safety_score = (self.get_peroxability_score() + self.get_ignition_temp_score() + self.get_flash_point_score() + self.get_resistivity_score())
        return safety_score

    def calculate_health_score(self):
        if self.reach:
            health_score = self.calculate_hazard_score(get_health_code_dict())
            if self.boiling_point < 85:
                health_score += 1
        else:
            health_score = 5
        return health_score

    def calculate_environment_score(self):
        if self.reach:
            env_score = self.calculate_hazard_score(get_env_code_dict())
            if env_score == 0:
                env_score = 3
        else:
            env_score = 5
        bp_score = self.get_bp_score()
        if bp_score < env_score:
            return env_score
        else:
            return bp_score

    def calculate_hazard_score(self, code_dict):
        score = []
        for worst, codes in code_dict.items():
            if len([x for x in self.hazard_codes if x in codes]) >= 1:
                score.append(worst)
        try:
            return max(score)
        except ValueError:
            return 0

    def get_bp_score(self):
        if 50 < self.boiling_point < 69:
            bp_score = 5
        elif 70 < self.boiling_point < 140:
            bp_score = 3
        elif 141 < self.boiling_point < 200:
            bp_score = 5
        else:
            bp_score = 7
        return bp_score

    def countX(self, lst, x):
        return lst.count(x)

    def calculate_CHEM21_score(self, she_list):
        count8 = self.countX(she_list, 8)
        count7 = self.countX(she_list, 7)
        count46 = len([x for x in she_list if 3 < x < 7])
        if count8 >= 1:
            return 3
        elif count7 >= 2:
            return 3
        elif count7 == 1:
            return 2
        if count46 >= 2:
            return 2
        else:
            return 1

    def calculate_all(self):
        safety_score = self.calculate_safety_score()
        health_score = self.calculate_health_score()
        env_score = self.calculate_environment_score()
        CHEM21 = self.calculate_CHEM21_score([safety_score, health_score, env_score])
        return {'CHEM21_score': CHEM21, 'safety_score': safety_score, 'health_score': health_score, 'environment_score': env_score}



