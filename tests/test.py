from unittest import TestCase
from gql_query_builder import GqlQuery


class TestGqlQuery(TestCase):
    def test_query_a_single_field(self):
        expected = 'query { hero { name } }'
        actual = GqlQuery().fields(['name']).query('hero').operation().generate()
        self.assertEqual(expected, actual)

    def test_query_neting_fields(self):
        expected = 'query { hero { name friends { name } } }'
        field_friends = GqlQuery().fields(['name'], name='friends').generate()
        actual = GqlQuery().fields(['name', field_friends]).query('hero').operation('query').generate()
        self.assertEqual(expected, actual)

    def test_query_input(self):
        expected = 'query { human(id: "1000") { name height } }'
        actual = GqlQuery().fields(['name', 'height']).query('human', input={"id": '"1000"'}).operation().generate()
        self.assertEqual(expected, actual)

    def test_query_with_nested_input(self):
        expected = 'query { human(input: {data: {id: "1000", name: "test"}}) { name height } }'
        actual = GqlQuery().fields(['name', 'height']).query('human', input={
            "input": {"data": {"id": "1000", "name": "test"}}}).operation().generate()
        print(actual)
        self.assertEqual(expected, actual)

    def test_query_input_with_arguments(self):
        expected = 'query { human(id: "1000") { name height(unit: FOOT) } }'
        actual = GqlQuery().fields(['name', 'height(unit: FOOT)']).query(
            'human', input={"id": '"1000"'}).operation().generate()
        self.assertEqual(expected, actual)

    def test_query_alias(self):
        expected = 'query { empireHero: hero(episode: EMPIRE) { name } jediHero: hero(episode: JEDI) { name } }'
        query_empirehero = GqlQuery().fields(['name']).query(
            'hero', alias='empireHero', input={"episode": 'EMPIRE'}).generate()
        query_jedihero = GqlQuery().fields(['name']).query(
            'hero', alias='jediHero', input={"episode": 'JEDI'}).generate()
        actual = GqlQuery().operation('query', queries=[query_empirehero, query_jedihero]).generate()
        self.assertEqual(expected, actual)

    def test_fragment(self):
        expected = 'fragment comparisonFields on Character { name appearsIn friends { name } }'
        field_friends = GqlQuery().fields(['name'], name='friends').generate()
        actual = GqlQuery().fields(['name', 'appearsIn', field_friends]).fragment(
            'comparisonFields', 'Character').generate()
        self.assertEqual(expected, actual)

    def test_refer_to_fragment(self):
        expected = 'query { leftComparison: hero(episode: EMPIRE) { ...comparisonFields } rightComparison: hero(episode: JEDI) { ...comparisonFields } }'
        query_leftComparison = GqlQuery().fields(['...comparisonFields']).query(
            'hero', alias='leftComparison', input={"episode": "EMPIRE"}).generate()
        query_rightComparison = GqlQuery().fields(['...comparisonFields']).query(
            'hero', alias='rightComparison', input={"episode": "JEDI"}).generate()
        actual = GqlQuery().operation('query', queries=[query_leftComparison, query_rightComparison]).generate()
        self.assertEqual(expected, actual)

    def test_query_with_variables(self):
        expected = 'query HeroNameAndFriends($episode: Episode) { hero(episode: $episode) { name friends { name } } }'
        field_friends = GqlQuery().fields(['name'], name='friends').generate()
        actual = GqlQuery().fields(['name', field_friends]).query('hero', input={"episode": "$episode"}).operation(
            'query', name='HeroNameAndFriends', input={"$episode": "Episode"}).generate()
        self.assertEqual(expected, actual)

    def test_query_directives(self):
        expected = 'query Hero($episode: Episode, $withFriends: Boolean!) { hero(episode: $episode) { name friends @include(if: $withFriends) { name } } }'
        field_friends = GqlQuery().fields(['name'], name='friends @include(if: $withFriends)').generate()
        actual = GqlQuery().fields(['name', field_friends]).query('hero', input={"episode": "$episode"}).operation(
            'query', name='Hero', input={"$episode": "Episode", "$withFriends": "Boolean!"}).generate()
        self.assertEqual(expected, actual)

    def test_mutation(self):
        expected = 'mutation CreateReviewForEpisode($ep: Episode!, $review: ReviewInput!) { createReview(episode: $ep, review: $review) { stars commentary } }'
        actual = GqlQuery().fields(['stars', 'commentary']).query('createReview', input={"episode": "$ep",
                                                                                         "review": "$review"}).operation(
            'mutation', name='CreateReviewForEpisode', input={"$ep": "Episode!", "$review": "ReviewInput!"}).generate()
        self.assertEqual(expected, actual)

    def test_remove_duplicate_spaces(self):
        expected = '{ query { hero { name } } }'
        actual = GqlQuery().remove_duplicate_spaces(' {  query  {  hero  {  name  }  }  } ')
        self.assertEqual(expected, actual)
